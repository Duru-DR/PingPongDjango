import re
from django.core.exceptions import ValidationError

def validate_lowercase_and_digits(string):
    pattern = re.compile(r'^[a-z0-9]{8}$')
    if not pattern.match(string):
        raise ValidationError('The string must be exactly 8 characters long and include only lowercase letters and digits.')
    return string
