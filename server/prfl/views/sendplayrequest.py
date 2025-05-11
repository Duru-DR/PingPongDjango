from rest_framework                 import generics, status
from django.http                    import JsonResponse
from authentication.utils           import Authenticate
from channels.layers                import get_channel_layer
from asgiref.sync                   import async_to_sync
from ..models                       import FriendRequest, Profile, Notification
from ..utils.connections_manager    import connected_clients, clients_lock 

class SendPlayWithMeRequestView(generics.GenericAPIView):
    def post(self, request):
        print("^__________")
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
                {"message": "User does not exist"},
                status = status.HTTP_404_NOT_FOUND
            )
    
        if profile in user.profile.play_requests.all() or profile in user.profile.received_play_requests.all():
            return JsonResponse(
                {"message": f"You have already sent/receive a PlayWithMe request to/from {username}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.profile.play_requests.add(profile)

        Notification.objects.create(
            profile=profile,
            content=f"You have a PLAYWITHME request from {user.username}", 
            notification_type='PLAYWITHME_REQUEST',
            from_user=user.username
        )
        channel_layer = get_channel_layer()
        async_to_sync(self.handle_request)(user.username, username, channel_layer)
        return JsonResponse(
            {"message": "PlayWithMe Request sent successfully"},
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
                        "type": "send_playwithme_request",
                        "from": username1,
                    }
                )