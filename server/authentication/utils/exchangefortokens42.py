import requests
from datetime       import datetime, timezone, timedelta
from django.conf    import settings

def ExchangeForTokens42(code):
    client_id = settings.INTRA_CLIENT_ID
    client_secret = settings.INTRA_CLIENT_SECRET
    redirect_uri = 'http://localhost:8800/api/auth/intra42/callback/' #settings['GOOGLE_REDIRECT_URI']
    url = 'https://api.intra.42.fr/oauth/token'
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