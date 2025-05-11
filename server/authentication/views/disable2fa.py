from rest_framework import generics, permissions, status 
from django.http import JsonResponse
from ..utils import Authenticate 
from ..models import CustomTOTPDevice

class Disable2fa(generics.GenericAPIView):
    
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        device = CustomTOTPDevice.objects.get(user=user, confirmed=True)
        if not device:
            return JsonResponse(
                {"message": "no totp device found for this user"},
                status = status.HTTP_404_NOT_FOUND
            )
        try:
            device.delete()
            user.is_2fa_enabled = False
            user.save()
            return JsonResponse(
                {"message": "2FA has been disabled"}, 
                status=status.HTTP_200_OK
            )
        except CustomTOTPDevice.DoesNotExist:
            return JsonResponse(
                {"message": "No confirmaed TOTP device found"}, 
                status=status.HTTP_404_NOT_FOUND
            )