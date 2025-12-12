#!/usr/bin/env python3
"""
Script to create notification templates for the Library Management System
Run this from the notification service directory:
python3 create_templates.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_notifications_service.settings')
django.setup()

from notifications.models import NotificationTemplate

# Template 1: Loan Creation
loan_created_template = NotificationTemplate.objects.update_or_create(
    name='loan_created',
    defaults={
        'type': 'EMAIL',
        'subject_template': '📚 Confirmation d\'emprunt - Bibliothèque',
        'message_template': '''Bonjour,

Nous vous confirmons l'emprunt du livre suivant :

📖 DÉTAILS DU LIVRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Titre : {{ book_title }}
• Auteur : {{ book_author|default:"Non spécifié" }}
• ISBN : {{ book_isbn|default:"Non spécifié" }}
• Catégorie : {{ book_category|default:"Non spécifiée" }}

📅 INFORMATIONS D'EMPRUNT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Date d'emprunt : {{ loan_date }}
• Date de retour prévue : {{ due_date }}
• Durée : 14 jours
• Numéro d'emprunt : #{{ loan_id }}

⚠️ RAPPEL IMPORTANT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Merci de retourner le livre avant le {{ due_date }}.
En cas de retard, une amende de 50 DZD par jour sera appliquée.

Vous pouvez renouveler votre emprunt jusqu'à 2 fois si le livre n'est pas réservé par un autre utilisateur.

Cordialement,
L'équipe de la Bibliothèque''',
        'description': 'Email sent when a new loan is created',
        'is_active': True
    }
)

# Template 2: Loan Return (On Time)
loan_returned_ontime_template = NotificationTemplate.objects.update_or_create(
    name='loan_returned_ontime',
    defaults={
        'type': 'EMAIL',
        'subject_template': '✅ Retour confirmé - Bibliothèque',
        'message_template': '''Bonjour,

Nous confirmons le retour du livre suivant :

📖 DÉTAILS DU LIVRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Titre : {{ book_title }}
• Numéro d'emprunt : #{{ loan_id }}

📅 INFORMATIONS DE RETOUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Date de retour : {{ return_date }}
• Date prévue : {{ due_date }}
• Statut : ✅ Retour dans les délais

Merci d'avoir respecté les délais de retour !

Cordialement,
L'équipe de la Bibliothèque''',
        'description': 'Email sent when a book is returned on time',
        'is_active': True
    }
)

# Template 3: Loan Return (Late with Fine)
loan_returned_late_template = NotificationTemplate.objects.update_or_create(
    name='loan_returned_late',
    defaults={
        'type': 'EMAIL',
        'subject_template': '✅ Retour confirmé - Bibliothèque',
        'message_template': '''Bonjour,

Nous confirmons le retour du livre suivant :

📖 DÉTAILS DU LIVRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Titre : {{ book_title }}
• Numéro d'emprunt : #{{ loan_id }}

📅 INFORMATIONS DE RETOUR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Date de retour : {{ return_date }}
• Date prévue : {{ due_date }}
• Retard : {{ days_overdue }} jour(s)

💰 AMENDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Montant : {{ fine_amount }} DZD
• Tarif : 50 DZD par jour de retard

⚠️ RAPPEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Merci de régler cette amende auprès de la bibliothèque dans les plus brefs délais.

Cordialement,
L'équipe de la Bibliothèque''',
        'description': 'Email sent when a book is returned late with a fine',
        'is_active': True
    }
)

# Template 4: Loan Renewal
loan_renewed_template = NotificationTemplate.objects.update_or_create(
    name='loan_renewed',
    defaults={
        'type': 'EMAIL',
        'subject_template': '🔄 Renouvellement confirmé - Bibliothèque',
        'message_template': '''Bonjour,

Votre emprunt a été renouvelé avec succès !

📖 DÉTAILS DU LIVRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Titre : {{ book_title }}
• Numéro d'emprunt : #{{ loan_id }}

🔄 INFORMATIONS DE RENOUVELLEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Nombre de renouvellements : {{ renewal_count }}/2
• Ancienne date de retour : {{ old_due_date }}
• Nouvelle date de retour : {{ new_due_date }}
• Durée supplémentaire : 14 jours

⚠️ RAPPEL IMPORTANT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Merci de retourner le livre avant le {{ new_due_date }}.
En cas de retard, une amende de 50 DZD par jour sera appliquée.

{{ renewal_message }}

Cordialement,
L'équipe de la Bibliothèque''',
        'description': 'Email sent when a loan is renewed',
        'is_active': True
    }
)

print("✅ Templates created successfully!")
print(f"  - {loan_created_template[0].name} ({'created' if loan_created_template[1] else 'updated'})")
print(f"  - {loan_returned_ontime_template[0].name} ({'created' if loan_returned_ontime_template[1] else 'updated'})")
print(f"  - {loan_returned_late_template[0].name} ({'created' if loan_returned_late_template[1] else 'updated'})")
print(f"  - {loan_renewed_template[0].name} ({'created' if loan_renewed_template[1] else 'updated'})")
