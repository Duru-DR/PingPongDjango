from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from prfl.models                   import Profile

class DataView(generics.GenericAPIView):

    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        username = request.data.get('username')
        if not username:
            return JsonResponse(
                {"message": "Username is required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            profile = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return JsonResponse(
                {"message": "User not found"},
                status = status.HTTP_404_NOT_FOUND
            )
        profile_data = {
            "username": profile.username,
            "picture": profile.picture if profile.picture else None,
            "rank": profile.rank,
        }

        return JsonResponse(
            profile_data,
            status = status.HTTP_200_OK,
        )