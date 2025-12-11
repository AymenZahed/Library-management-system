from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import requests
import logging
import os
from typing import Optional, Dict, Any

from .models import Loan, LoanHistory
from .serializers import LoanSerializer, LoanCreateSerializer, LoanHistorySerializer
from .permissions import (
    IsAuthenticated, CanBorrowBook, CanViewLoans, 
    CanViewAllLoans, CanManageLoans, IsLibrarianOrAdmin
)
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_notification(user_id, notification_type, subject, message, token=None):
    """Helper to send notifications via Notification Service"""
    headers = {}
    if token:
        if token.lower().startswith('bearer '):
            headers['Authorization'] = token
        else:
            headers['Authorization'] = f"Bearer {token}"
        logger.debug(f"Sending notification with token: {token[:20]}...")
    else:
        logger.warning("Sending notification WITHOUT token - this may fail!")
            
    try:
        response = requests.post(
            f"{settings.SERVICES.get('NOTIFICATION_SERVICE', 'http://localhost:8004')}/api/notifications/",
            json={
                'user_id': user_id,
                'type': notification_type,
                'subject': subject,
                'message': message
            },
            headers=headers,
            timeout=5
        )
        if response.status_code != 201:
            logger.error(f"Notification failed: {response.status_code} - {response.text}")
        return response.status_code == 201
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        return False

# ============================================
#    SERVICE CLIENTS
# ============================================

class UserServiceClient:
    """
    Client HTTP pour communiquer avec le User Service
    """
    
    def __init__(self):
        self.base_url = os.getenv('USER_SERVICE_URL', 'http://localhost:8001')
        self.timeout = 10  # secondes
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupérer les informations d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Dict avec les infos de l'utilisateur ou None si erreur
        """
        url = f"{self.base_url}/api/users/{user_id}/"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"✅ User {user_id} trouvé: {user_data.get('username')}")
                return user_data
            elif response.status_code == 404:
                logger.warning(f"❌ User {user_id} non trouvé")
                return None
            else:
                logger.error(f"❌ Erreur User Service: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout lors de l'appel User Service pour user {user_id}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur de connexion User Service: {e}")
            return None
    
    def is_user_active(self, user_id: int) -> bool:
        """
        Vérifier si un utilisateur est actif
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            True si actif, False sinon
        """
        user_data = self.get_user(user_id)
        if not user_data:
            return False
        
        return user_data.get('is_active', False)
    
    def get_user_email(self, user_id: int) -> Optional[str]:
        """
        Récupérer l'email d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur
            
        Returns:
            Email ou None
        """
        user_data = self.get_user(user_id)
        if not user_data:
            return None
        
        return user_data.get('email')


class BookServiceClient:
    """
    Client HTTP pour communiquer avec le Books Service
    """
    
    def __init__(self):
        self.base_url = os.getenv('BOOK_SERVICE_URL', 'http://localhost:8002')
        self.timeout = 10
    
    def get_book(self, book_id: int) -> Optional[Dict[str, Any]]:
        """
        Récupérer les informations d'un livre.
        
        Args:
            book_id: ID du livre
            
        Returns:
            Dict avec les infos du livre ou None si erreur
        """
        url = f"{self.base_url}/api/books/{book_id}/"
        
        try:
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                book_data = response.json()
                logger.info(f"✅ Book {book_id} trouvé: {book_data.get('title')}")
                return book_data
            elif response.status_code == 404:
                logger.warning(f"❌ Book {book_id} non trouvé")
                return None
            else:
                logger.error(f"❌ Erreur Books Service: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"⏱️ Timeout Books Service pour book {book_id}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur connexion Books Service: {e}")
            return None
    
    def check_availability(self, book_id: int) -> bool:
        """
        Vérifier si un livre est disponible.
        
        Args:
            book_id: ID du livre
            
        Returns:
            True si disponible, False sinon
        """
        book_data = self.get_book(book_id)
        if not book_data:
            return False
        
        available_copies = book_data.get('available_copies', 0)
        return available_copies > 0
    
    def get_available_copies(self, book_id: int) -> int:
        """
        Récupérer le nombre d'exemplaires disponibles.
        
        Args:
            book_id: ID du livre
            
        Returns:
            Nombre d'exemplaires disponibles
        """
        book_data = self.get_book(book_id)
        if not book_data:
            return 0
        
        return book_data.get('available_copies', 0)
    
    def decrement_stock(self, book_id: int, token: str = None) -> bool:
        """
        Décrémenter le stock d'un livre (emprunt).
        
        Note: The Books Service should have an endpoint like:
        POST /api/books/{id}/borrow/
        
        For now, we'll use the borrow endpoint if it exists.
        
        Args:
            book_id: ID du livre
            token: JWT token for authentication
            
        Returns:
            True si succès, False sinon
        """
        url = f"{self.base_url}/api/books/{book_id}/borrow/"
        headers = {}
        if token:
            headers['Authorization'] = f"Bearer {token}"
        
        try:
            response = requests.post(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                logger.info(f"✅ Stock décrémenté pour book {book_id}")
                return True
            else:
                logger.error(f"❌ Erreur décrémentation: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur décrémentation stock: {e}")
            return False
    
    def increment_stock(self, book_id: int, token: str = None) -> bool:
        """
        Incrémenter le stock d'un livre (retour).
        
        Note: The Books Service should have an endpoint like:
        POST /api/books/{id}/return/
        
        Args:
            book_id: ID du livre
            token: JWT token for authentication
            
        Returns:
            True si succès, False sinon
        """
        url = f"{self.base_url}/api/books/{book_id}/return/"
        headers = {}
        if token:
            headers['Authorization'] = f"Bearer {token}"
        
        try:
            response = requests.post(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                logger.info(f"✅ Stock incrémenté pour book {book_id}")
                return True
            else:
                logger.error(f"❌ Erreur incrémentation: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur incrémentation stock: {e}")
            return False


# ============================================
#    HEALTH CHECK
# ============================================

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint."""
    return Response({
        'status': 'healthy',
        'service': 'loans',
        'timestamp': timezone.now()
    })


# ============================================
#    US7: EMPRUNTER UN LIVRE
# ============================================

@api_view(['POST'])
@permission_classes([IsAuthenticated, CanBorrowBook])
def create_loan(request):
    """
    Create a new loan (borrow a book).
    
    POST /api/loans/
    
    Required permissions: can_borrow_book
    """
    create_serializer = LoanCreateSerializer(data=request.data)
    if not create_serializer.is_valid():
        return Response(
            {
                'error': 'Données invalides',
                'details': create_serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user_id = create_serializer.validated_data['user_id']
    book_id = create_serializer.validated_data['book_id']
    notes = create_serializer.validated_data.get('notes', '')
    
    # Verify user can only borrow for themselves (unless librarian/admin)
    if not request.user.is_librarian() and not request.user.is_admin():
        if user_id != request.user.id:
            return Response(
                {'error': 'Vous ne pouvez emprunter que pour vous-même'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    user_client = UserServiceClient()
    book_client = BookServiceClient()
    
    # 1. Verify user exists and is active
    if not user_client.is_user_active(user_id):
        return Response(
            {'error': 'Utilisateur introuvable ou inactif'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 2. Verify book exists and is available
    book_data = book_client.get_book(book_id)
    if not book_data:
        return Response(
            {'error': 'Livre introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if book_data.get('available_copies', 0) <= 0:
        return Response(
            {
                'error': 'Livre indisponible',
                'available_copies': 0,
                'book_title': book_data.get('title')
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 3. Verify user has less than 5 active loans
    active_loans_count = Loan.objects.filter(
        user_id=user_id,
        status__in=['ACTIVE', 'RENEWED', 'OVERDUE']
    ).count()
    
    if active_loans_count >= 5:
        return Response(
            {
                'error': 'Quota d\'emprunts dépassé',
                'active_loans': active_loans_count,
                'max_loans': 5
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 4. Verify user doesn't already have this book
    if Loan.objects.filter(
        user_id=user_id,
        book_id=book_id,
        status__in=['ACTIVE', 'RENEWED', 'OVERDUE']
    ).exists():
        return Response(
            {'error': 'Vous avez déjà emprunté ce livre'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 5. Create loan with transaction
    try:
        with transaction.atomic():
            # Calculate due_date (loan_date + 14 days)
            loan_date = timezone.now().date()
            due_date = loan_date + timedelta(days=14)
            
            loan = Loan.objects.create(
                user_id=user_id,
                book_id=book_id,
                loan_date=loan_date,
                due_date=due_date,
                notes=notes,
                status='ACTIVE'
            )
            
            # 6. Decrement book stock (pass auth token)
            auth_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
            if not book_client.decrement_stock(book_id, token=auth_token):
                raise Exception("Échec de la décrémentation du stock")
            
            # 7. Create audit log
            LoanHistory.objects.create(
                loan_id=loan.id,
                action='CREATED',
                performed_by=request.user.id,
                details=f"Emprunt créé pour le livre '{book_data.get('title')}'"
            )
            
            serializer = LoanSerializer(loan)
            
            # Send professional notification email
            auth_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
            user_email = user_client.get_user_email(user_id)
            user_name = f"{book_data.get('title', 'Utilisateur')}"
            
            email_subject = '📚 Confirmation d\'emprunt - Bibliothèque'
            email_message = f"""
Bonjour,

Nous vous confirmons l'emprunt du livre suivant :

📖 DÉTAILS DU LIVRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Titre : {book_data.get('title')}
• Auteur : {book_data.get('author', 'Non spécifié')}
• ISBN : {book_data.get('isbn', 'Non spécifié')}
• Catégorie : {book_data.get('category', 'Non spécifiée')}

📅 INFORMATIONS D'EMPRUNT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Date d'emprunt : {loan.loan_date.strftime('%d/%m/%Y')}
• Date de retour prévue : {loan.due_date.strftime('%d/%m/%Y')}
• Durée : 14 jours
• Numéro d'emprunt : #{loan.id}

⚠️ RAPPEL IMPORTANT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Merci de retourner le livre avant le {loan.due_date.strftime('%d/%m/%Y')}.
En cas de retard, une amende de 50 DZD par jour sera appliquée.

Vous pouvez renouveler votre emprunt jusqu'à 2 fois si le livre n'est pas réservé par un autre utilisateur.

Cordialement,
L'équipe de la Bibliothèque
            """.strip()
            
            send_notification(
                user_id=user_id,
                notification_type='EMAIL',
                subject=email_subject,
                message=email_message,
                token=auth_token
            )
            return Response(
                {
                    'message': 'Emprunt créé avec succès',
                    'loan': serializer.data,
                    'book_title': book_data.get('title'),
                    'due_date': loan.due_date.strftime('%d/%m/%Y')
                },
                status=status.HTTP_201_CREATED
            )
    except Exception as e:
        logger.error(f"Erreur lors de la création de l'emprunt: {e}")
        return Response(
            {'error': 'Erreur lors de la création de l\'emprunt'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============================================
#    US8: RETOURNER UN LIVRE
# ============================================

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanBorrowBook])
def return_loan(request, pk):
    """
    Return a borrowed book.
    
    PUT /api/loans/{id}/return/
    
    Required permissions: can_borrow_book
    """
    try:
        loan = Loan.objects.get(id=pk)
    except Loan.DoesNotExist:
        return Response(
            {'error': 'Emprunt non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verify user can only return their own loans (unless librarian/admin)
    if not request.user.is_librarian() and not request.user.is_admin():
        if loan.user_id != request.user.id:
            return Response(
                {'error': 'Vous ne pouvez retourner que vos propres emprunts'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    # Verify loan is active or overdue
    if loan.status not in ['ACTIVE', 'OVERDUE', 'RENEWED']:
        return Response(
            {'error': f'Ce livre a déjà été retourné (statut: {loan.status})'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    book_client = BookServiceClient()
    
    try:
        with transaction.atomic():
            # Mark as returned and calculate fine if overdue
            return_date = timezone.now().date()
            loan.return_date = return_date
            loan.status = 'RETURNED'
            
            # Calculate fine if overdue (50 DZD per day)
            fine_amount = 0
            if return_date > loan.due_date:
                days_overdue = (return_date - loan.due_date).days
                fine_amount = days_overdue * 50
                loan.fine_amount = fine_amount
            
            loan.save()
            
            # Increment book stock (pass auth token)
            auth_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
            if not book_client.increment_stock(loan.book_id, token=auth_token):
                raise Exception("Échec de l'incrémentation du stock")
            
            # Create audit log
            details = f"Livre retourné"
            if fine_amount > 0:
                details += f" avec {days_overdue} jour(s) de retard. Amende: {fine_amount} DZD"
            
            LoanHistory.objects.create(
                loan_id=loan.id,
                action='RETURNED',
                performed_by=request.user.id,
                details=details
            )
            
            serializer = LoanSerializer(loan)
            response_data = {
                'message': 'Livre retourné avec succès',
                'loan': serializer.data
            }
            
            if fine_amount > 0:
                response_data['fine'] = {
                    'amount': fine_amount,
                    'days_overdue': days_overdue,
                    'message': f'Amende de {fine_amount} DZD pour {days_overdue} jour(s) de retard'
                }
                
            message = f'Livre retourné avec succès.'
            if fine_amount > 0:
                message += f' Amende: {fine_amount} DZD pour {days_overdue} jour(s) de retard.'
            
            # Send professional return notification
            auth_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
            book_data_return = book_client.get_book(loan.book_id)
            
            email_subject = '✅ Retour confirmé - Bibliothèque'
            if fine_amount > 0:
                email_message = f"""
Bonjour,

Nous confirmons le retour du livre suivant :

📖 DÉTAILS DU LIVRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Titre : {book_data_return.get('title') if book_data_return else 'Non disponible'}
• Numéro d'emprunt : #{loan.id}

📅 INFORMATIONS DE RETOUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Date de retour : {loan.return_date.strftime('%d/%m/%Y')}
• Date prévue : {loan.due_date.strftime('%d/%m/%Y')}
• Retard : {days_overdue} jour(s)

💰 AMENDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Montant : {fine_amount} DZD
• Tarif : 50 DZD par jour de retard

⚠️ RAPPEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Merci de régler cette amende auprès de la bibliothèque dans les plus brefs délais.

Cordialement,
L'équipe de la Bibliothèque
                """.strip()
            else:
                email_message = f"""
Bonjour,

Nous confirmons le retour du livre suivant :

📖 DÉTAILS DU LIVRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Titre : {book_data_return.get('title') if book_data_return else 'Non disponible'}
• Numéro d'emprunt : #{loan.id}

📅 INFORMATIONS DE RETOUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Date de retour : {loan.return_date.strftime('%d/%m/%Y')}
• Date prévue : {loan.due_date.strftime('%d/%m/%Y')}
• Statut : ✅ Retour dans les délais

Merci d'avoir respecté les délais de retour !

Cordialement,
L'équipe de la Bibliothèque
                """.strip()
            
            send_notification(
                user_id=request.user.id,
                notification_type='EMAIL',
                subject=email_subject,
                message=email_message,
                token=auth_token
            )
            
            return Response(response_data, status=status.HTTP_200_OK)
            
    except Exception as e:
        logger.error(f"Erreur lors du retour: {e}")
        return Response(
            {'error': 'Erreur lors du retour du livre'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ============================================
#    US9: RENOUVELER UN EMPRUNT
# ============================================

@api_view(['PUT'])
@permission_classes([IsAuthenticated, CanBorrowBook])
def renew_loan(request, pk):
    """
    Renew a loan (extend due date by 14 days).
    
    PUT /api/loans/{id}/renew/
    
    Max 2 renewals. Cannot renew if overdue.
    Required permissions: can_borrow_book
    """
    try:
        loan = Loan.objects.get(id=pk)
    except Loan.DoesNotExist:
        return Response(
            {'error': 'Emprunt non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verify user can only renew their own loans (unless librarian/admin)
    if not request.user.is_librarian() and not request.user.is_admin():
        if loan.user_id != request.user.id:
            return Response(
                {'error': 'Vous ne pouvez renouveler que vos propres emprunts'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    # Verify loan status is ACTIVE (not OVERDUE, not RETURNED)
    if loan.status != 'ACTIVE' and loan.status != 'RENEWED':
        return Response(
            {'error': f'Impossible de renouveler: statut {loan.status}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify not overdue
    if loan.is_overdue():
        return Response(
            {'error': 'Impossible de renouveler un emprunt en retard'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify renewal count < max_renewals (2)
    if loan.renewal_count >= loan.max_renewals:
        return Response(
            {
                'error': 'Nombre maximum de renouvellements atteint',
                'renewal_count': loan.renewal_count,
                'max_renewals': loan.max_renewals
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Renew loan
    loan.due_date = loan.due_date + timedelta(days=14)
    loan.renewal_count += 1
    loan.status = 'RENEWED'
    loan.save()
    
    # Create audit log
    LoanHistory.objects.create(
        loan_id=loan.id,
        action='RENEWED',
        performed_by=request.user.id,
        details=f"Renouvellement #{loan.renewal_count}. Nouvelle date de retour: {loan.due_date}"
    )
    
    serializer = LoanSerializer(loan)
    auth_token = request.META.get('HTTP_AUTHORIZATION', '').replace('Bearer ', '')
    book_client = BookServiceClient()
    book_data_renew = book_client.get_book(loan.book_id)
    
    email_subject = '🔄 Renouvellement confirmé - Bibliothèque'
    email_message = f"""
Bonjour,

Votre emprunt a été renouvelé avec succès !

📖 DÉTAILS DU LIVRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Titre : {book_data_renew.get('title') if book_data_renew else 'Non disponible'}
• Numéro d'emprunt : #{loan.id}

🔄 INFORMATIONS DE RENOUVELLEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Nombre de renouvellements : {loan.renewal_count}/2
• Ancienne date de retour : {(loan.due_date - timedelta(days=14)).strftime('%d/%m/%Y')}
• Nouvelle date de retour : {loan.due_date.strftime('%d/%m/%Y')}
• Durée supplémentaire : 14 jours

⚠️ RAPPEL IMPORTANT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Merci de retourner le livre avant le {loan.due_date.strftime('%d/%m/%Y')}.
En cas de retard, une amende de 50 DZD par jour sera appliquée.

{f'Vous pouvez encore renouveler cet emprunt {2 - loan.renewal_count} fois.' if loan.renewal_count < 2 else 'Attention : Vous avez atteint le nombre maximum de renouvellements (2).'}

Cordialement,
L'équipe de la Bibliothèque
    """.strip()
    
    send_notification(
        user_id=request.user.id,
        notification_type='EMAIL',
        subject=email_subject,
        message=email_message,
        token=auth_token
    )
    return Response(
        {
            'message': 'Emprunt renouvelé avec succès',
            'loan': serializer.data,
            'new_due_date': loan.due_date.strftime('%d/%m/%Y'),
            'renewals_remaining': loan.max_renewals - loan.renewal_count
        },
        status=status.HTTP_200_OK
    )


# ============================================
#    US9: CONSULTER EMPRUNTS
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, CanViewLoans])
def user_loans(request, user_id):
    """
    Get all loans for a specific user (history).
    
    GET /api/loans/user/{user_id}/
    
    Required permissions: can_view_loans
    """
    # Verify user can only view their own loans (unless librarian/admin)
    if not request.user.is_librarian() and not request.user.is_admin():
        if user_id != request.user.id:
            return Response(
                {'error': 'Vous ne pouvez consulter que vos propres emprunts'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    loans = Loan.objects.filter(user_id=user_id).order_by('-created_at')
    serializer = LoanSerializer(loans, many=True)
    
    return Response({
        'count': loans.count(),
        'loans': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, CanViewLoans])
def user_active_loans(request, user_id):
    """
    Get active loans for a specific user.
    
    GET /api/loans/user/{user_id}/active/
    
    Required permissions: can_view_loans
    """
    # Verify user can only view their own loans (unless librarian/admin)
    if not request.user.is_librarian() and not request.user.is_admin():
        if user_id != request.user.id:
            return Response(
                {'error': 'Vous ne pouvez consulter que vos propres emprunts'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    loans = Loan.objects.filter(
        user_id=user_id,
        status__in=['ACTIVE', 'RENEWED', 'OVERDUE']
    ).order_by('-created_at')
    
    serializer = LoanSerializer(loans, many=True)
    
    return Response({
        'count': loans.count(),
        'active_loans': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, CanViewAllLoans])
def active_loans(request):
    """
    Get all active loans (LIBRARIAN only).
    
    GET /api/loans/active/
    
    Required permissions: can_view_all_loans
    """
    loans = Loan.objects.filter(
        status__in=['ACTIVE', 'RENEWED', 'OVERDUE']
    ).order_by('-created_at')
    
    serializer = LoanSerializer(loans, many=True)
    
    return Response({
        'count': loans.count(),
        'active_loans': serializer.data
    })


# ============================================
#    US10: EMPRUNTS EN RETARD
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, CanViewAllLoans])
def overdue_loans(request):
    """
    Get all overdue loans (LIBRARIAN/ADMIN only).
    
    GET /api/loans/overdue/
    
    Required permissions: can_view_all_loans
    """
    today = timezone.now().date()
    loans = Loan.objects.filter(
        due_date__lt=today,
        status__in=['ACTIVE', 'RENEWED', 'OVERDUE']
    ).order_by('due_date')
    
    serializer = LoanSerializer(loans, many=True)
    
    return Response({
        'count': loans.count(),
        'overdue_loans': serializer.data
    })


# ============================================
#    GENERIC ENDPOINTS
# ============================================

@api_view(['GET'])
@permission_classes([IsAuthenticated, CanViewAllLoans])
def loan_list(request):
    """
    Get all loans (LIBRARIAN/ADMIN only).
    
    GET /api/loans/list/
    
    Required permissions: can_view_all_loans
    """
    loans = Loan.objects.all().order_by('-created_at')
    serializer = LoanSerializer(loans, many=True)
    
    return Response({
        'count': loans.count(),
        'loans': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated, CanViewLoans])
def loan_detail(request, pk):
    """
    Get loan details.
    
    GET /api/loans/{id}/
    
    Required permissions: can_view_loans
    """
    try:
        loan = Loan.objects.get(id=pk)
    except Loan.DoesNotExist:
        return Response(
            {'error': 'Emprunt non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verify user can only view their own loans (unless librarian/admin)
    if not request.user.is_librarian() and not request.user.is_admin():
        if loan.user_id != request.user.id:
            return Response(
                {'error': 'Vous ne pouvez consulter que vos propres emprunts'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    serializer = LoanSerializer(loan)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, CanViewLoans])
def loan_history(request, pk):
    """
    Get loan history (audit log).
    
    GET /api/loans/{id}/history/
    
    Required permissions: can_view_loans
    """
    try:
        loan = Loan.objects.get(id=pk)
    except Loan.DoesNotExist:
        return Response(
            {'error': 'Emprunt non trouvé'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Verify user can only view their own loans (unless librarian/admin)
    if not request.user.is_librarian() and not request.user.is_admin():
        if loan.user_id != request.user.id:
            return Response(
                {'error': 'Vous ne pouvez consulter que vos propres emprunts'},
                status=status.HTTP_403_FORBIDDEN
            )
    
    history = LoanHistory.objects.filter(loan_id=pk).order_by('-created_at')
    serializer = LoanHistorySerializer(history, many=True)
    
    return Response({
        'loan_id': pk,
        'history': serializer.data
    })
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsLibrarianOrAdmin])
def send_overdue_notifications(request):
    """Send notifications to all users with overdue loans"""
    today = timezone.now().date()
    overdue_loans = Loan.objects.filter(
        due_date__lt=today,
        status__in=['ACTIVE', 'RENEWED', 'OVERDUE']
    )
    
    sent_count = 0
    for loan in overdue_loans:
        days_overdue = (today - loan.due_date).days
        fine = days_overdue * 50
        
        if send_notification(
            user_id=loan.user_id,
            notification_type='EMAIL',
            subject='Emprunt en retard',
            message=f'Votre emprunt est en retard de {days_overdue} jour(s). Amende: {fine} DZD. Veuillez retourner le livre rapidement.'
        ):
            sent_count += 1
    
    return Response({
        'message': f'Notifications envoyées à {sent_count} utilisateur(s)',
        'total_overdue': overdue_loans.count()
    })