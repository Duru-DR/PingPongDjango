from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from django.db.models           import Q
from ..models                   import Profile, Friend
from ..utils                    import friendslist

class UserProfileView(generics.GenericAPIView):

    def get(self, request, username):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
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
            "badge": profile.badge,
            "background_picture": profile.background_picture if profile.background_picture else None,
            "wins": profile.wins,
            "loses": profile.loses,
            "friends": friendslist(profile)
        }
    
        return JsonResponse(
            profile_data,
            status = status.HTTP_200_OK,
        )