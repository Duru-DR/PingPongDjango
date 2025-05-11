from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import AuthenticationFailed
from ..models import CustomUser  
import jwt

class CustomJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        print(request.user)
        # print(request.user.username)
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None

        try:
            payload = jwt.decode(access_token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Access token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')

        print("11111")
        try:
            print(payload['jti'])
            user = CustomUser.objects.get(id=payload['user_id'])
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)
