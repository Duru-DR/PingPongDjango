import requests

def GetDataGG(token):
    end_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(end_url, headers=headers)
    return response.json()