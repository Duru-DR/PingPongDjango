from rest_framework import generics, status
from django.shortcuts import redirect
from django.http import JsonResponse
from datetime import datetime, timezone, timedelta
import jwt
import uuid
from django.conf import settings
from ..utils import (
    ExchangeForTokensGG,
    GetDataGG,
    AuthenticateUserGG,
    JWTsGenerator,
    print_red,
    print_green,
    print_yellow,
)

class GoogleOAuthView(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        try:
            authorization_code = request.GET.get("code") 
            print_red(f'code----- {authorization_code}')
            token = ExchangeForTokensGG(authorization_code)
            print(f'tokens***** {token}')
            userData = GetDataGG(token)
            print_green(f'data===== {userData}')
        except Exception as e:
            return redirect(f'http://localhost:8080/oauth?param=0')
        id = AuthenticateUserGG(request, userData)
        expr = datetime.now(timezone.utc) + timedelta(minutes=5)
        token = jwt.encode(
            payload= {
                'exp': expr,
                'user_id': id,
                'jti': str(uuid.uuid4()),
            },
            key= settings.SIMPLE_JWT['SIGNING_KEY'],
            algorithm='HS256'
        )
        return redirect(f'http://localhost:8080/oauth?param={str(token)}')