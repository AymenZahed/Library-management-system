"""
Comprehensive tests for User, UserProfile, Permission, and Group models
adapted for email-only User model without username/first_name/last_name.
"""

import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from users.models import UserProfile, Permission, Group

User = get_user_model()

# ============================================

# USER MODEL TESTS

# ============================================

@pytest.mark.django_db
class TestUserModel:


    def test_create_user(self):
        """Test creating a basic user."""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        assert user.email == 'test@example.com'
        assert user.check_password('testpass123')
        assert user.role == 'MEMBER'  # Default role
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.role == 'ADMIN'

    def test_user_email_unique(self):
        """Test email must be unique."""
        User.objects.create_user(email='duplicate@example.com', password='pass123')
        with pytest.raises(IntegrityError):
            User.objects.create_user(email='duplicate@example.com', password='pass123')

def test_user_str_representation(self):
    """Test user string representation."""
    user = User.objects.create_user(email='user@example.com', password='pass123')
    assert str(user) == f"{getattr(user, 'username', '')} ({user.get_role_display()})"


# ============================================

# USER PROFILE TESTS

# ============================================

@pytest.mark.django_db
class TestUserProfile:

    def test_create_profile(self):
        user = User.objects.create_user(email='profile@example.com', password='pass123')
        profile = UserProfile.objects.create(user=user, bio='Test bio', address='123 St')
        assert profile.user == user
        assert profile.bio == 'Test bio'
        assert profile.address == '123 St'

    def test_profile_one_to_one(self):
        user = User.objects.create_user(email='profile2@example.com', password='pass123')
        UserProfile.objects.create(user=user)
        with pytest.raises(IntegrityError):
            UserProfile.objects.create(user=user)


# ============================================

# PERMISSION TESTS

# ============================================

@pytest.mark.django_db
class TestPermission:

    def test_create_permission(self):
        perm = Permission.objects.create(code='test_perm', name='Test Permission')
        assert perm.code == 'test_perm'
        assert perm.name == 'Test Permission'

    def test_permission_code_unique(self):
        Permission.objects.create(code='unique_perm', name='Unique Permission')
        with pytest.raises(IntegrityError):
            Permission.objects.create(code='unique_perm', name='Another Permission')

# ============================================

# GROUP TESTS

# ============================================

@pytest.mark.django_db
class TestGroup:


    def test_create_group_and_add_permissions(self):
        group = Group.objects.create(name='Test Group')
        perm1 = Permission.objects.create(code='perm1', name='P1')
        perm2 = Permission.objects.create(code='perm2', name='P2')
        group.permissions.set([perm1, perm2])
        assert group.permissions.count() == 2
        codes = group.get_permission_codes()
        assert 'perm1' in codes and 'perm2' in codes

