"""
Custom password validators for enhanced security
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_password_strength(password):
    """
    Validate password strength:
    - At least 8 characters
    - Contains uppercase and lowercase letters
    - Contains at least one digit
    - Contains at least one special character
    """
    errors = []
    
    if len(password) < 8:
        errors.append(_("Password must be at least 8 characters long."))
    
    if not re.search(r'[A-Z]', password):
        errors.append(_("Password must contain at least one uppercase letter."))
    
    if not re.search(r'[a-z]', password):
        errors.append(_("Password must contain at least one lowercase letter."))
    
    if not re.search(r'\d', password):
        errors.append(_("Password must contain at least one digit."))
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append(_("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."))
    
    if errors:
        raise ValidationError(errors)
    
    return password

