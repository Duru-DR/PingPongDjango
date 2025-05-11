from rest_framework import generics, status
from django.http import JsonResponse
from django.core.cache import cache
from ..serializers import CustomUserSerializer
from ..utils import Authenticate
import hashlib

def invalidatetoken(request, message):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        hashed_token = hashlib.sha256(refresh_token.encode()).hexdigest()
        cache.set(hashed_token, 'BlackListedToken', 30)
        response = JsonResponse(
            {"message": message}, 
            status=status.HTTP_200_OK
        )
        response.delete_cookie(
            key='access_token', 
            samesite='None'
        )
        response.delete_cookie(
            key='refresh_token',
            samesite='None'
        )
        return response
    else:
        return JsonResponse(
            {"message": 'No refresh token found.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )