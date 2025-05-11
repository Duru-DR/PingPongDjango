from rest_framework import generics, status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from .decodeJWT import decodeJWTToken
import jwt

User = get_user_model()

def Authenticate(request):
        id = request.META['USER_ID']
        if not id:
            return AnonymousUser()
        return User.objects.get(id=id)