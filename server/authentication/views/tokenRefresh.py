from django.http import JsonResponse
from rest_framework import generics, status
from ..utils import JWTsGenerator, decodeJWTToken, print_green, print_red
from ..serializers import CustomUserSerializer
from django.core.cache import cache
import hashlib
class TokenRefreshView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    
    def get(self, request, *args, **kwargs):
        print_green('Refreshing tokens ')
        refresh_tok = request.COOKIES.get('refresh_token')

        if not refresh_tok:
            return JsonResponse(
                {"message": "No Token available"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        token = decodeJWTToken(refresh_tok)
        if not token:
            return JsonResponse(
                {"message": "Invalid token"},
                status = status.HTTP_400_BAD_REQUEST
            )
        id = token['user_id']
        cache.set(hashlib.sha256(refresh_tok.encode()).hexdigest(), 'BlackListedToken')
        return JWTsGenerator(
            id,
            {"message": "Successful refreshing"}
        )