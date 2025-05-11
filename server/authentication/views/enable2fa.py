from rest_framework import generics, permissions, status
from django.http import JsonResponse
from ..utils import Authenticate 
from ..models import CustomTOTPDevice
import qrcode
import base64
from io import BytesIO

class Enable2fa(generics.GenericAPIView):
    
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        devices = CustomTOTPDevice.objects.filter(user=user)
        # To delete this part
        for device in devices:
            device.delete()
        # --------------------
        device = CustomTOTPDevice.objects.filter(user=user).first()
        if device:
            return JsonResponse(
                {"message": "2FA is Already Enabled"},
                status=status.HTTP_409_CONFLICT
            )
        device = CustomTOTPDevice.objects.create(user=user)
        url = device.config_url
        qr = qrcode.make(url)
        buffer = BytesIO()
        qr.save(buffer)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        user.save()
        return JsonResponse(
            {"qr_code": qr_base64},
            status=status.HTTP_200_OK
        )