"""
Tests for JWT and Role middleware
Covers security aspects of authentication and authorization
"""
import pytest
from django.test import RequestFactory, TestCase
from django.http import JsonResponse
from books_service.middleware import JWTMiddleware, RoleMiddleware


class JWTMiddlewareTests(TestCase):
    """Test JWT authentication middleware"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = lambda request: JsonResponse({'success': True})
        self.middleware = JWTMiddleware(self.get_response)
    
    def test_middleware_blocks_request_without_token(self):
        """Middleware should block requests without Authorization header"""
        request = self.factory.get('/api/books/')
        response = self.middleware.process_request(request)
        
        assert response is not None
        assert response.status_code == 401
        assert 'error' in response.json()
    
    def test_middleware_allows_request_with_token(self):
        """Middleware should allow requests with Authorization header"""
        request = self.factory.get('/api/books/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer fake-token-123'
        response = self.middleware.process_request(request)
        assert response is None
    
    def test_middleware_blocks_empty_token(self):
        """Middleware should block requests with empty Authorization header"""
        request = self.factory.get('/api/books/')
        request.META['HTTP_AUTHORIZATION'] = ''
        response = self.middleware.process_request(request)
        
        assert response is not None
        assert response.status_code == 401
    
    def test_middleware_handles_different_http_methods(self):
        """Middleware should work consistently across HTTP methods"""
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        
        for method in methods:
            request = getattr(self.factory, method.lower())('/api/books/')
            response = self.middleware.process_request(request)
            assert response is not None
            assert response.status_code == 401


class RoleMiddlewareTests(TestCase):
    """Test role-based authorization middleware"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.get_response = lambda request: JsonResponse({'success': True})
        self.middleware = RoleMiddleware(self.get_response)
    
    def test_middleware_processes_request(self):
        """Role middleware should process requests"""
        request = self.factory.get('/api/books/')
        response = self.middleware.process_request(request)
        assert response is None
    
    def test_middleware_handles_authenticated_request(self):
        """Role middleware should handle authenticated requests"""
        request = self.factory.get('/api/books/')
        request.user = type('User', (), {'is_authenticated': True, 'id': 1})()
        response = self.middleware.process_request(request)
        assert response is None


@pytest.mark.django_db
class MiddlewareSecurityTests:
    """Security-focused tests for middleware"""
    
    @pytest.fixture
    def factory(self):
        return RequestFactory()
    
    @pytest.fixture
    def jwt_middleware(self):
        return JWTMiddleware(lambda r: JsonResponse({'success': True}))
    
    def test_sql_injection_in_token(self, factory, jwt_middleware):
        """Middleware should safely handle SQL injection attempts in token"""
        request = factory.get('/api/books/')
        request.META['HTTP_AUTHORIZATION'] = "'; DROP TABLE users; --"
        response = jwt_middleware.process_request(request)
        assert response is None
    
    def test_xss_in_token(self, factory, jwt_middleware):
        """Middleware should safely handle XSS attempts in token"""
        request = factory.get('/api/books/')
        request.META['HTTP_AUTHORIZATION'] = '<script>alert("xss")</script>'
        response = jwt_middleware.process_request(request)
        assert response is None
    
    def test_very_long_token(self, factory, jwt_middleware):
        """Middleware should handle extremely long tokens"""
        request = factory.get('/api/books/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + 'A' * 10000
        response = jwt_middleware.process_request(request)
        assert response is None


class MiddlewareEdgeCasesTests(TestCase):
    """Edge cases and boundary conditions"""
    
    def setUp(self):
        self.factory = RequestFactory()
        self.jwt_middleware = JWTMiddleware(lambda r: JsonResponse({'success': True}))
    
    def test_middleware_with_options_request(self):
        """Middleware should handle OPTIONS requests"""
        request = self.factory.options('/api/books/')
        response = self.jwt_middleware.process_request(request)
        assert response is not None
        assert response.status_code == 401
    
    def test_middleware_with_authorization_header(self):
        """Middleware should specifically check Authorization header"""
        request = self.factory.get('/api/books/')
        request.META['HTTP_AUTHORIZATION'] = 'Bearer test-token'
        response = self.jwt_middleware.process_request(request)
        assert response is None