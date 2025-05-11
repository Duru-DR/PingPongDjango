from rest_framework import generics, permissions, status
from django.http import JsonResponse
from rest_framework.views import APIView
from ..models import CustomTOTPDevice
from ..utils import Authenticate, JWTsGenerator

class VerifyDevice(generics.GenericAPIView):
    
    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        otp_code = request.data.get('otp_code')
        if not otp_code:
            return JsonResponse(
                {"message": "OTP code is required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        device = CustomTOTPDevice.objects.get(user=user)
        if not device:
            return JsonResponse(
                {"message": "no totp device found for this user"},
                status = status.HTTP_404_NOT_FOUND
            )
        if device.verify_token(otp_code):
            device.confirmed = True
            device.save()
            user.is_2fa_enabled = True
            user.save()
            return JsonResponse(
                {"message": "Successfull Validation"},
                status=status.HTTP_200_OK
            ) 
        return JsonResponse(
            {"message": "Invalid verification code"},
            status=status.HTTP_400_BAD_REQUEST
        )
