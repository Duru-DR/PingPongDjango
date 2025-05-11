from rest_framework import generics, permissions, status
from django.http import JsonResponse
from ..utils import Authenticate, print_green, print_yellow
from ..models import CustomTOTPDevice

class GenerateBackupCodes(generics.GenericAPIView):
    def get(self, request):
        print_green('generating backup Codes')
        user = Authenticate(request)

        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        device = CustomTOTPDevice.objects.get(user=user)
        if not device:
            return JsonResponse(
                {"message": "no totp device found for this user"},
                status = status.HTTP_404_NOT_FOUND
            )
        backup_codes = device.generate_backup_codes()
        print_yellow(f'the Codes: {backup_codes}')
        return JsonResponse(
            {"backup_codes": backup_codes},
            status=status.HTTP_200_OK
        )