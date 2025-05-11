from ..utils import Authenticate 
from rest_framework import generics, permissions, status
from django.http import JsonResponse

class VerifyPasswd(generics.GenericAPIView):
    def post(self, request):
        user = Authenticate(request)
        passwd = request.data.get('password')
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_400_BAD_REQUEST
            )
        if not passwd:
            return JsonResponse(
                {"message": "Password is required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        if user.check_password(passwd):
            return JsonResponse(
                {"message": "Valid Password"},
                status=status.HTTP_200_OK
            )
        return JsonResponse(
            {"message": "Invalid password"},
            status=status.HTTP_400_BAD_REQUEST
        )