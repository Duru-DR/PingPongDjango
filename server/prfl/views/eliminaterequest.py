from rest_framework                 import generics, status
from django.http                    import JsonResponse
from authentication.utils           import Authenticate
from django.db.models               import Q
from ..models                       import FriendRequest, Profile, Notification, BlockedFriend

class EliminateFriendshipRequestView(generics.GenericAPIView):
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
        if username == user.username:
            return JsonResponse(
                {"message": "This operation is forbidden on yourself"},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            profile = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist"},
                status = status.HTTP_404_NOT_FOUND
            )
        try:
            friend_request = FriendRequest.objects.get(from_user=user.profile, to_user=profile)
            friend_request.delete()
        except FriendRequest.DoesNotExist:
            return JsonResponse(
                {"message": "Friendship Request does not exist"},
                status = status.HTTP_404_NOT_FOUND
            )

        return JsonResponse(
            {"message": "Friendship Request eliminated successfully"},
            status = status.HTTP_200_OK
        )