from rest_framework                 import generics, status
from django.http                    import JsonResponse
from authentication.utils           import Authenticate
from channels.layers                import get_channel_layer
from asgiref.sync                   import async_to_sync
from ..models                       import FriendRequest, Profile, Notification
from ..utils.connections_manager    import connected_clients, clients_lock 

class SendJoinTournamentNotificationView(generics.GenericAPIView):
    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        username = request.data.get('username')
        tournament_name = request.data.get('tournament_name')
        if not username or not tournament_name:
            return JsonResponse(
                {"message": "Username and tournament name are required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        try: 
            profile = Profile.objects.get(username=username)
        except Profile.DoesNotExist:
            return JsonResponse(
                {"message": "User does not exist"},
                status = status.HTTP_404_NOT_FOUND
            )
        Notification.objects.create(
            profile=profile, 
            content=f"The tournament {tournament_name} has started! Join now, {user.username}.", 
            notification_type='JOINING_TOURNAMENT',
            from_user=user.username
        )
        channel_layer = get_channel_layer()
        async_to_sync(self.handle_request)(user.username, username, tournament_name, channel_layer)
        return JsonResponse(
            {"message": "Tournament joining notification sent successfully."},
            status = status.HTTP_200_OK
        )

    async def handle_request(self, username1, username2, tournament_name, channel_layer):
        async with clients_lock:
            channel_name = connected_clients.get(username2)
            if channel_name:
                print(":::::::::::: Sending ........")
                await channel_layer.send(
                    channel_name,
                    {
                        "type": "join_tournament_notification",
                        "from": username1,
                        "tournament_name": tournament_name,
                    }
                )
