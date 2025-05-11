import re
from django.core.exceptions import ValidationError

def validate_six_digits(code):
    pattern = re.compile(r'^\d{6}$')
    if not pattern.match(code):
        raise ValidationError('The code must be exactly 6 digits long.')
    return code
