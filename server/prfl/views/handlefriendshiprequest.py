from rest_framework                 import generics, status
from django.http                    import JsonResponse
from authentication.utils           import Authenticate
from channels.layers                import get_channel_layer
from asgiref.sync                   import async_to_sync
from ..models                       import FriendRequest, Profile, Notification, Friend
from ..utils.connections_manager    import connected_clients, clients_lock 

class HandleFriendshipRequestView(generics.GenericAPIView):
    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        username = request.data.get('username')
        status_ = request.data.get('status')
        if not username or not status:
            return JsonResponse(
                {"message": "Username and status are required"},
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
            friendshiprequest = FriendRequest.objects.get(from_user=profile, to_user=user.profile)
            friendshiprequest.delete()
        except FriendRequest.DoesNotExist:
            return JsonResponse(
                {"message": "This friendship request does not exist"},
                status = status.HTTP_404_NOT_FOUND
            )
        if status_ == 'accepted':
            Friend.objects.create(profile=profile, friend=user.profile)
        Notification.objects.create(
            profile=profile, 
            content=f"{user.username} has {status_} your FriendShip request", 
            notification_type='HANDLE_REQUESTED_FRIENDSHIP',
            from_user=user.username
        )
        channel_layer = get_channel_layer()
        async_to_sync(self.handle_request)(user.username, username, channel_layer, status_)
        
        return JsonResponse(
            {"message": "Friendship request handled successfully"},
            status = status.HTTP_200_OK
        )

    async def handle_request(self, username1, username2, channel_layer, status):
        async with clients_lock:
            channel_name = connected_clients.get(username2)
            if channel_name:
                print(":::::::::::: Sending ........")
                await channel_layer.send(
                    channel_name,
                    {
                        "type": "handle_friendship_request",
                        "from": username1,
                        "status": status
                    }
                )