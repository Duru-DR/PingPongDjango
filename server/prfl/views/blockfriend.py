from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from chat.models                import Chat
from ..models                   import Profile, BlockedFriend
from ..utils                    import get_friendship

class BlockFriendView(generics.GenericAPIView):
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
            to_block = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist"},
                status = status.HTTP_404_NOT_FOUND
            )
        if to_block == user.profile:
            return JsonResponse(
                {"message": "Cannot block yourself"},
                status = status.HTTP_400_BAD_REQUEST
            )
        friendship = get_friendship(user.profile, to_block)
        if friendship:
            friendship.delete()
        try:
            BlockedFriend.objects.get(blocker=user.profile, blocked_friend=to_block)
            return JsonResponse(
                {"message": "User is already blocked"},
                status = status.HTTP_400_BAD_REQUEST,
            )
        except BlockedFriend.DoesNotExist:
            pass
    
        BlockedFriend.objects.create(blocker=user.profile, blocked_friend=to_block)
        
        try:
            chat = Chat.objects.get(
                user1__in=[user.profile, to_block], 
                user2__in=[user.profile, to_block]
            )
            chat.delete()
        except Chat.DoesNotExist:
            pass


        return JsonResponse(
            {"message": "User blocked successfully"},
            status = status.HTTP_200_OK,
        )