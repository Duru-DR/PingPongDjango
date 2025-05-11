from rest_framework import generics, permissions, status
from django.http import JsonResponse
from rest_framework.views import APIView
from ..models import CustomTOTPDevice
from ..utils import JWTsGenerator
from django.contrib.auth import get_user_model

User = get_user_model()

class Verify2fa(generics.GenericAPIView):
    
    def post(self, request):
        otp_code = request.data.get('otp_code')
        id = request.data.get('user_id')
        if not otp_code or not id:
            return JsonResponse(
                {"message": "OTP code is required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist"},
                status = status.HTTP_400_BAD_REQUEST
            )
        device = CustomTOTPDevice.objects.get(user=user)
        if not device:
            return JsonResponse(
                {"message": "No User found"},
                status=status.HTTP_404_NOT_FOUND
            )
        if device.verify_backup_code(otp_code):
            return JWTsGenerator(
                id,
                {"message": "Successfull Validation"}
            )
        if device.verify_token(otp_code):
            device.confirmed = True
            device.save()
            return JWTsGenerator(
                id,
                {"message": "Successfull Validation"}
            )
        return JsonResponse(
            {"message": "Invalid verification code"},
            status=status.HTTP_400_BAD_REQUEST
        )
