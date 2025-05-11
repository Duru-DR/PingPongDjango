from rest_framework     import generics, status
from django.shortcuts   import redirect
from datetime           import datetime, timezone, timedelta
from django.conf        import settings
from ..utils            import (
    ExchangeForTokens42,
    GetData42,
    AuthenticateUser42,
    print_red,
    print_green,
    print_yellow,
)
import jwt
import uuid

class IntraOAuthView(generics.GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        try:
            print_green('_--------------------------')
            authorization_code = request.GET.get("code")
            print_red(f'code----- {authorization_code}')
            token = ExchangeForTokens42(authorization_code)
            print(f'tokens***** {token}')
            userData = GetData42(token)
            print_green(f'data===== {userData}')
        except Exception as e:
            print_yellow(f'Error: {str(e)}')
            return redirect('http://localhost:8080/oauth?param=0')
        id = AuthenticateUser42(request, userData)
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
        print(f'>>>>>> {id}')
        return redirect(f'http://localhost:8080/oauth?param={str(token)}')