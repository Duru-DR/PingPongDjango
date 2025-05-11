from django.contrib.auth    import authenticate, login
from django.http            import JsonResponse 
from rest_framework         import generics, status, permissions
from django.conf            import settings
from ..serializers          import CustomUserSerializer
from ..models               import CustomUser
from django.core.cache      import cache
from ..utils                import (
    JWTsGenerator, 
    decodeJWTToken,
    Authenticate,
    print_red, 
    print_green, 
    print_yellow
)
import hashlib

class TokenView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all() 
    
    def get(self, request, *args, **kwargs):
        print_yellow(f"DOES ID keep-------- ")
        user = Authenticate(request)
        if user.is_authenticated:
            return JsonResponse(
                {"message": "Successful Authentication"}, 
                status = status.HTTP_200_OK
            )
        return JsonResponse(
            {"message": "User not authenticated"}, 
            status = status.HTTP_401_UNAUTHORIZED
        )

    def post(self, request, *args, **kwargs):
        # Authenticate with credentials
        print_green('Token/ Validate with credentials')
        username = request.data.get('username')
        password = request.data.get('password')
        print_yellow(f'username: {username} Pass: {password}')
        if (not (username and password)):
            return JsonResponse(
                {"message": "Username and Password are required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse(
                {"message": "Invalid Credentials"},
                status = status.HTTP_400_BAD_REQUEST
            )

        # Authenticate with 2fa
        print_red(f'Is 2fa Enabled: {user.is_2fa_enabled}')
        if user.is_2fa_enabled:
            return JsonResponse(
                {
                    "is_2fa_enabled": True,
                    "user_id": user.id
                },
                status = status.HTTP_200_OK
            )
        if not user.is_2fa_enabled:
            return JWTsGenerator(
                user.id,
                {"is_2fa_enabled": False}
            )

