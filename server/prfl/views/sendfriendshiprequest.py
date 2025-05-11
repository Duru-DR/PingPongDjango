from rest_framework                 import generics, status
from django.http                    import JsonResponse
from authentication.utils           import Authenticate
from channels.layers                import get_channel_layer
from asgiref.sync                   import async_to_sync
from django.db.models               import Q
from ..models                       import FriendRequest, Profile, Notification, BlockedFriend, Friend
from ..utils.connections_manager    import connected_clients, clients_lock 

class SendFriendshipRequestView(generics.GenericAPIView):
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
                {"message": "You cannot send a friendship request to yourself"},
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
            Friend.objects.get(
                Q(profile=user.profile, friend=profile) |
                Q(profile=profile, friend=user.profile)
            )
            return JsonResponse (
                {"message": f"You are already a friend with {username}."},
                status = status.HTTP_400_BAD_REQUEST
            )
        except Friend.DoesNotExist:
            pass
        try:
            FriendRequest.objects.get(
                Q(from_user=user.profile, to_user=profile) |
                Q(from_user=profile, to_user=user.profile)
            )
            return JsonResponse (
                {"message": f"You've already sent a friendship request, or {username} has already sent one."},
                status = status.HTTP_400_BAD_REQUEST
            )
        except FriendRequest.DoesNotExist:
            pass
        try:
            BlockedFriend.objects.get(
                Q(blocker=user.profile, blocked_friend=profile) |
                Q(blocker=profile, blocked_friend=user.profile)
            )
            return JsonResponse (
                {"message": f"You've already blocked this user or {username} has blocked you."},
                status = status.HTTP_400_BAD_REQUEST
            )
        except BlockedFriend.DoesNotExist:
            pass
        FriendRequest.objects.create(from_user=user.profile, to_user=profile)
        Notification.objects.create(
            profile=profile, 
            content=f"You have a FriendShip request from {user.username}", 
            notification_type='FRIENDSHIP_REQUEST',
            from_user=user.username
        )
        channel_layer = get_channel_layer()
        async_to_sync(self.handle_request)(user.username, username, channel_layer)
        
        return JsonResponse(
            {"message": "Friendship Request sent successfully"},
            status = status.HTTP_200_OK
        )

    async def handle_request(self, username1, username2, channel_layer):
        async with clients_lock:
            channel_name = connected_clients.get(username2)
            if channel_name:
                print(":::::::::::: Sending ........")
                await channel_layer.send(
                    channel_name,
                    {
                        "type": "send_friendship_request",
                        "from": username1,
                    }
                )