"""
Custom throttle classes for user authentication endpoints
"""
from rest_framework.throttling import SimpleRateThrottle


class RegisterThrottle(SimpleRateThrottle):
    """Throttle for registration endpoint - 5 requests per hour per IP"""
    scope = 'register'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # Don't throttle authenticated users
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class LoginThrottle(SimpleRateThrottle):
    """Throttle for login endpoint - 10 requests per hour per IP"""
    scope = 'login'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None  # Don't throttle authenticated users
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class PasswordResetThrottle(SimpleRateThrottle):
    """Throttle for password reset endpoint - 3 requests per hour per IP"""
    scope = 'password_reset'
    
    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class EmailVerificationThrottle(SimpleRateThrottle):
    """Throttle for email verification endpoint - 10 requests per hour per IP"""
    scope = 'email_verification'
    
    def get_cache_key(self, request, view):
        ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class CommentThrottle(SimpleRateThrottle):
    """Throttle for comment creation - 20 requests per hour per user"""
    scope = 'comment'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.id
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }

