from django.utils.deprecation   import MiddlewareMixin
from django.http                import JsonResponse
from django.core.cache          import cache
from django.conf                import settings
from rest_framework             import status
from django.contrib.auth        import get_user_model
from rest_framework.exceptions  import AuthenticationFailed
from .utils                     import decodeJWTToken, print_green, print_red, print_yellow
import hashlib

User = get_user_model()

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print_green('Token/ With ')
        if not (request.method == 'POST' and request.path in ['/api/auth/signup/', '/api/auth/token/']):
            refresh_tok = request.COOKIES.get('refresh_token')
            access_tok =  request.COOKIES.get('access_token')
    
            if not refresh_tok or not access_tok:
                print_red('does not exist')
                request.META['USER_ID'] = None
            else:
                if refresh_tok:
                    print_red('Refresh token exist')
                    hashed_token = hashlib.sha256(refresh_tok.encode()).hexdigest()
                    if cache.get(hashed_token):
                        print_red('User legged out / From refresh token')
                        return JsonResponse(
                                {"message": "Invalid Token"},
                                status = status.HTTP_401_UNAUTHORIZED
                        )
                if access_tok:
                    print_red('Acces token exist')
                    payload = decodeJWTToken(access_tok)
                    if not payload:
                        print_red('Invalid')
                        response = JsonResponse(
                            {"message": "Invalid Token"},
                            status = status.HTTP_403_FORBIDDEN
                        )
                        response.delete_cookie(
                            key='access_token', 
                            samesite='None'
                        )
                        return response
                    id = payload['user_id']
                    print(id)
                    if id:
                        try:
                            user = User.objects.get(id=id)
                            print_red('**************************')
    
                            if user.token_last_change and payload['iat'] < int(user.token_last_change.timestamp()):
                                raise AuthenticationFailed('Token has been invalidated.')
                        except User.DoesNotExist:
                            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
                            return JsonResponse(
                                {"message": "Invalid Token"},
                                status = status.HTTP_401_UNAUTHORIZED
                            )
    
                        request.META['USER_ID'] = str(id)
    
            print_yellow("++++++++++++++++++++++++++++")
            