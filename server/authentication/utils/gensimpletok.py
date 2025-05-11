from datetime               import datetime, timezone, timedelta
from django.conf            import settings
import jwt
import uuid

def gen_token(user):
    expr = datetime.now(timezone.utc) + timedelta(hours=1)
    token = jwt.encode(
        payload= {
            'exp': expr,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'jti': str(uuid.uuid4()),
        },
        key= settings.SIMPLE_JWT['SIGNING_KEY'],
        algorithm='HS256'
    )
    return token