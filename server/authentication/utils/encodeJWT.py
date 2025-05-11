
import jwt
import uuid
from datetime import datetime, timezone, timedelta
from django.conf import settings

def createJWTToken(user, tokenLifetime):
    payload = {
        'sub': str(user.id),
        'exp': datetime.now(timezone.utc) + tokenLifetime,
        'user_id': user.id,
        'iat': datetime.now(timezone.utc),
        'jti': str(uuid.uuid4()),
        'username': user.username,
        'is_staff': user.is_staff,
    }
    print(f'here PAYLOAD------ {payload}')
    token = jwt.encode(payload, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm='HS256')
    return token
