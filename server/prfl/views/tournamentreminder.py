from rest_framework                 import generics, status
from django.http                    import JsonResponse
from authentication.utils           import Authenticate
from channels.layers                import get_channel_layer
from asgiref.sync                   import async_to_sync
from ..models                       import FriendRequest, Profile, Notification
from ..utils.connections_manager    import connected_clients, clients_lock 

class TournamentReminderNotificationView(generics.GenericAPIView):
    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        usernames = request.data.get('usernames', [])
        if not usernames:
            return JsonResponse(
                {"message": "Please provide the usernames to send the notification."},
                status = status.HTTP_400_BAD_REQUEST
            )
        profiles = Profile.objects.filter(username__in=usernames)
        print(profiles)
        if not profiles.exists():
            return JsonResponse(
                {"message": "No profiles found for the provided usernames."},
                status=status.HTTP_404_NOT_FOUND
            )

        channel_layer = get_channel_layer()

        for profile in profiles:
            Notification.objects.create(
                profile=profile,
                content=f"The tournament has started! Join now, {profile}.",
                notification_type='TOURNAMENT_REMINDER',
            )

            async_to_sync(self.handle_request)(
                profile, channel_layer
            )

        return JsonResponse(
            {"message": "Tournament reminder notification sent successfully."},
            status=status.HTTP_200_OK
        )

    async def handle_request(self, username1, channel_layer):
        async with clients_lock:
            channel_name = connected_clients.get(username1)
            if channel_name:
                print(":::::::::::: Sending ........")
                await channel_layer.send(
                    channel_name,
                    {
                        "type": "tournament_reminder_notification"
                    }
                )