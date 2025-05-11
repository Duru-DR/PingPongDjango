import re
from django.core.exceptions import ValidationError

def validate_username(username):
    pattern = re.compile(r'^[a-zA-Z0-9_]{3,9}$')
    if not pattern.match(username):
        raise ValidationError('Username must be between 3 and 9 characters long and can contain letters, numbers, and underscores.')
    return username
