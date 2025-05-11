from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.util import random_hex
from . import BackupCode

class CustomTOTPDevice(TOTPDevice):
    def generate_backup_codes(self):
        backup_codes = []
        for _ in range(8):
            code = random_hex(4)
            BackupCode.objects.create(device=self, code=code)
            backup_codes.append(code)
        return backup_codes
    
    def verify_backup_code(self, code):
        try:
            backup_code = BackupCode.objects.get(device=self, code=code, used=False)
            backup_code.used = True
            backup_code.save()
            return True
        except BackupCode.DoesNotExist:
            return False