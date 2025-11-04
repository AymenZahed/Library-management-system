# backend/users/models.py

class User:
    """Classe User simple pour commencer"""
    
    def __init__(self, username, email, role="MEMBER"):
        self.username = username
        self.email = email
        self.role = role
        self.is_active = True
    
    def get_display_name(self):
        """Retourne le nom d'affichage"""
        return f"{self.username} ({self.role})"
    
    def can_borrow_books(self):
        """Vérifie si l'utilisateur peut emprunter des livres"""
        return self.is_active and self.role in ["MEMBER", "LIBRARIAN"]