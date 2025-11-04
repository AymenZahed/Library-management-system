# tests/test_users.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.users.models import User

def test_user_creation():
    """Test la création d'un utilisateur"""
    user = User("john_doe", "john@example.com", "MEMBER")
    
    assert user.username == "john_doe"
    assert user.email == "john@example.com"
    assert user.role == "MEMBER"
    assert user.is_active == True

def test_user_display_name():
    """Test le nom d'affichage"""
    user = User("alice", "alice@example.com", "LIBRARIAN")
    
    assert user.get_display_name() == "alice (LIBRARIAN)"

def test_user_can_borrow():
    """Test si l'utilisateur peut emprunter"""
    active_user = User("user1", "user1@example.com", "MEMBER")
    inactive_user = User("user2", "user2@example.com", "MEMBER")
    inactive_user.is_active = False
    
    assert active_user.can_borrow_books() == True
    assert inactive_user.can_borrow_books() == False