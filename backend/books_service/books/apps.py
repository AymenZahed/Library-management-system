from django.apps import AppConfig


import sys
import os
from django.apps import AppConfig
from django.conf import settings

class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'
    
    def ready(self):
        # Don't run this during static file collection or unrelated management commands
        if os.environ.get('RUN_MAIN') != 'true' and 'runserver' not in sys.argv:
            return
            
        # Add common directory to path for consul_utils import
        common_path = os.path.abspath(os.path.join(settings.BASE_DIR, '..', 'common'))
        if common_path not in sys.path:
            sys.path.insert(0, common_path)
            
        from consul_utils import register_service, deregister_service
        
        # Service configuration
        service_name = 'books-service'
        try:
            # Try to get port from runserver command or env var
            service_port = int(os.environ.get('SERVICE_PORT', 8002))
        except ValueError:
            service_port = 8002
            
        tags = ['django', 'books', 'backend']
        
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
