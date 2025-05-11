from channels.middleware        import BaseMiddleware
from channels.db                import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth        import get_user_model
from authentication.utils       import decodeJWTToken, print_green, print_red, print_yellow
import hashlib

User = get_user_model()

class TokenAuthenticationMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        print_red('websocket ... In middleware') 
        print_green(scope['headers'])
        headers = dict(scope['headers'])
        print_yellow(headers)
        cookies = headers.get(b'cookie', b'').decode()
        access_token = None
        print_green(cookies)
        if not cookies:
            return
        for item in cookies.split(';'):
            key, value = item.strip().split('=', 1)
            if key == 'access_token':
                access_token = value

        if access_token:
            payload = decodeJWTToken(access_token)
            if not payload:
                print_green('websocket ... Invalid token')
                scope['user'] = AnonymousUser()
            else:
                id = payload['user_id']
                if id:
                    try:
                        user = await database_sync_to_async(User.objects.get)(id=id)
                        scope['user'] = user
                    except User.DoesNotExist:
                        print_red('websocket ... User does not exist')
                        scope['user'] = AnonymousUser()
                else:
                    scope['user'] = AnonymousUser()

        else:
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)