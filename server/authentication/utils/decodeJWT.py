import jwt
from django.conf import settings

def decodeJWTToken(token):
    try:
        payload = jwt.decode(token, settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.exceptions.DecodeError:
        return None