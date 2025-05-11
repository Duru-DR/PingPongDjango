import re
from django.core.exceptions import ValidationError

def validate_email(email):
    pattern = re.compile(r'^[\w.-]+@([\w-]+\.)+[a-zA-Z]{2,8}$')
    if not pattern.match(email):
        raise ValidationError('Enter a valid email address.')
    return email
