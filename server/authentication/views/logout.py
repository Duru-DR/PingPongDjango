from rest_framework import generics, status
from django.http import JsonResponse
from django.core.cache import cache
from ..utils import Authenticate, invalidatetoken, print_green, print_red
import hashlib

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        print_green(f"User logging out {request.META['USER_ID']}")
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        return invalidatetoken(request, 'Successfully logged out.')