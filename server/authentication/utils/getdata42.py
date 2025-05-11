import requests

def GetData42(token):
    end_url = "https://api.intra.42.fr/v2/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(end_url, headers=headers)
    return response.json()