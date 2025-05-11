from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..models                   import Profile, BlockedFriend
from ..utils                    import get_friendship

class UnBlockFriendView(generics.GenericAPIView):
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
            blocked = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist"},
                status = status.HTTP_404_NOT_FOUND
            )
        if blocked == user.profile:
            return JsonResponse(
                {"message": "Cannot unblock yourself"},
                status = status.HTTP_400_BAD_REQUEST
            )
        try:
            to_unblock = BlockedFriend.objects.get(blocker=user.profile, blocked_friend=blocked)
        except BlockedFriend.DoesNotExist:
            return JsonResponse(
                {"message": "User is not blocked by you"},
                status = status.HTTP_400_BAD_REQUEST
            )
        to_unblock.delete()

        return JsonResponse(
            {"message": "User unblocked successfully"},
            status = status.HTTP_200_OK,
        )