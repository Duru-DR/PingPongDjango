from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.models import random_hex
from authentication.models.utils.validate_lower import validate_lowercase_and_digits

class BackupCode(models.Model):
    device = models.ForeignKey(TOTPDevice, on_delete=models.CASCADE, related_name='backup_codes')
    code = models.CharField(max_length=8, validators=[validate_lowercase_and_digits])
    used = models.BooleanField(default=False)