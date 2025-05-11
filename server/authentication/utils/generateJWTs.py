from django.http    import JsonResponse
from rest_framework import status
from django.conf    import settings
from .encodeJWT     import createJWTToken
from ..models       import CustomUser
from .print_color   import print_red, print_green, print_yellow

def JWTsGenerator(id, dic):
    print_green('GENERATING TOKENS')
    user = CustomUser.objects.get(id=id)
    access_token = createJWTToken(
            user, 
            settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    )
    refresh_token = createJWTToken(
            user, 
            settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
    )
    print_yellow(f'Access: {access_token} \n Refresh: {refresh_token}')
    response = JsonResponse(dic, status=status.HTTP_200_OK)
    # TODO: To check dates
    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=True,
        samesite='None',
        path='/'
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=True,
        samesite='None',
        path='/'
    )
    print_green('Successfully setted')
    return response