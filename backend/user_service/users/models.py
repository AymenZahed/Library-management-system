from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.


class User(models.Model):

    #Représente un utilisateur du système (Membre, Bibliothécaire, Admin)
    ROLE_CHOICES = [
        ('MEMBER', 'Member'),
        ('LIBRARIAN', 'librarian'),
        ('ADMIN', 'Admin'),
    ]
    
    # Attributs
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='MEMBER')
    is_active = models.BooleanField(default=True)
    max_loans = models.IntegerField(default=5)  # Nombre max d'emprunts simultanés
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def is_member(self):
        return self.role == 'MEMBER'
    
    def is_librarian(self):
        return self.role == 'LIBRARIAN'
    
    def is_admin(self):
        return self.role == 'ADMIN'
    
    def can_borrow(self):
        return self.is_active
    

class UserProfile(models.Model):
    """
    Profil détaillé associé à un utilisateur.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    avatar_url = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "user_profiles"
        ordering = ["user__username"]

    def __str__(self):
        return f"Profile de {self.user.username}"
