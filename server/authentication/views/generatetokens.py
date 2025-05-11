from rest_framework import generics, status, permissions
from django.conf    import settings
from django.http    import JsonResponse
from ..utils        import decodeJWTToken, JWTsGenerator, print_red, print_yellow

class GnrToken(generics.GenericAPIView):
    def post(self, request):
        token = decodeJWTToken(request.data.get("user_id"))
        if not token:
            return JsonResponse(
                {"error": "Invalid Token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        id = token.get('user_id')
        return JWTsGenerator(
            id,
            {"message": "Successfully generated"}
        )