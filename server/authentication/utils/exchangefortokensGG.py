import requests
from datetime       import datetime, timezone, timedelta
from django.conf    import settings

def ExchangeForTokensGG(code):
    client_id = settings.GOOGLE_CLIENT_ID
    client_secret = settings.GOOGLE_CLIENT_SECRET
    redirect_uri = 'http://localhost:8800/api/auth/google/callback/'
    url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    token = tokens.get('access_token')
    return token