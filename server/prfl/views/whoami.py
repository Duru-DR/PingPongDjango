from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate

class WhoAmI(generics.GenericAPIView):
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )

        return JsonResponse(
            {"username": user.username},
            status = status.HTTP_200_OK
        )
    