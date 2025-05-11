import re
from django.core.exceptions import ValidationError

def validate_name(name):
    pattern = re.compile(r'^[a-zA-Z-]{2,16}$')
    if not pattern.match(name):
        raise ValidationError('Name must be between 2 and 16 characters long and contain only letters and hyphens.')
    return name
