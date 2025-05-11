import re
from django.core.exceptions import ValidationError

def validate_password(password):
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})')
    if not pattern.match(password):
        raise ValidationError('Password must be at least 8 characters long and include at least one lowercase letter, one uppercase letter, one digit, and one special character.')
    return password
    