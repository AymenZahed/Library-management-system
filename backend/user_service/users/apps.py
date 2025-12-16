from django.apps import AppConfig
import sys
import os
from django.conf import settings

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """Auto-create groups and permissions on startup."""
        
        # Don't run this during static file collection or unrelated management commands
        if os.environ.get('RUN_MAIN') != 'true' and 'runserver' not in sys.argv:
            return

        # Add common directory to path for consul_utils import
        common_path = os.path.abspath(os.path.join(settings.BASE_DIR, '..', 'common'))
        if common_path not in sys.path:
            sys.path.insert(0, common_path)
            
        try:
            from consul_utils import register_service, deregister_service
            
            # Service configuration
            service_name = 'user-service'
            try:
                # Try to get port from runserver command or env var
                service_port = int(os.environ.get('SERVICE_PORT', 8001))
            except ValueError:
                service_port = 8001
                
            tags = ['django', 'users', 'backend']
            
            # Register service
            success, service_id = register_service(service_name, service_port, tags=tags)
            
            if success:
                self.service_id = service_id
                
                # Register shutdown handler
                import signal
                import atexit
                
                def shutdown_handler(*args, **kwargs):
                    deregister_service(service_id)
                    
                atexit.register(shutdown_handler)
                # Handle SIGTERM
                signal.signal(signal.SIGTERM, shutdown_handler)
                
        except ImportError:
            pass

        from django.db.utils import OperationalError, ProgrammingError
        
        try:
            self._create_default_permissions()
            self._create_default_groups()
        except (OperationalError, ProgrammingError):
            # Database not ready yet (during migrations)
            pass

    def _create_default_permissions(self):
        from .models import Permission
        
        # Define all permissions for the library system
        permissions = [
            # Book permissions
            ('can_view_books', 'Can View Books', 'BOOKS'),
            ('can_add_book', 'Can Add Book', 'BOOKS'),
            ('can_edit_book', 'Can Edit Book', 'BOOKS'),
            ('can_delete_book', 'Can Delete Book', 'BOOKS'),
            
            # Loan permissions
            ('can_view_loans', 'Can View Loans', 'LOANS'),
            ('can_borrow_book', 'Can Borrow Book', 'LOANS'),
            ('can_return_book', 'Can Return Book', 'LOANS'),
            ('can_view_all_loans', 'Can View All Loans', 'LOANS'),
            ('can_manage_loans', 'Can Manage All Loans', 'LOANS'),
            
            # User permissions
            ('can_view_users', 'Can View Users', 'USERS'),
            ('can_add_user', 'Can Add User', 'USERS'),
            ('can_edit_user', 'Can Edit User', 'USERS'),
            ('can_delete_user', 'Can Delete User', 'USERS'),
            
            # Report permissions
            ('can_view_reports', 'Can View Reports', 'REPORTS'),
            ('can_export_reports', 'Can Export Reports', 'REPORTS'),
        ]
        
        for code, name, category in permissions:
            Permission.objects.get_or_create(
                code=code,
                defaults={'name': name, 'category': category}
            )

    def _create_default_groups(self):
        from .models import Group, Permission
        
        # MEMBER group permissions
        member_perms = [
            'can_view_books',
            'can_borrow_book',
            'can_return_book',
            'can_view_loans',  # Own loans only
        ]
        
        # LIBRARIAN group permissions
        librarian_perms = [
            'can_view_books',
            'can_add_book',
            'can_edit_book',
            'can_delete_book',
            'can_view_all_loans',
            'can_manage_loans',
            'can_view_users',
            'can_view_reports',
        ]
        
        # Create MEMBER group
        member_group, _ = Group.objects.get_or_create(
            name='MEMBER',
            defaults={'description': 'Library members who can borrow books', 'is_default': True}
        )
        member_group.permissions.set(
            Permission.objects.filter(code__in=member_perms)
        )
        
        # Create LIBRARIAN group
        librarian_group, _ = Group.objects.get_or_create(
            name='LIBRARIAN',
            defaults={'description': 'Librarians who manage books and loans'}
        )
        librarian_group.permissions.set(
            Permission.objects.filter(code__in=librarian_perms)
        )
        
        # Create ADMIN group (all permissions)
        admin_group, _ = Group.objects.get_or_create(
            name='ADMIN',
            defaults={'description': 'Full system access'}
        )
        admin_group.permissions.set(Permission.objects.all())