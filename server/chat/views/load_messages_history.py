from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..models                   import Chat, Message
from prfl.models                import Profile
from django.db.models           import Q

class LoadMessagesView(generics.GenericAPIView):
    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        username = request.data.get('username')
        start = int(request.data.get('start', 0))
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
        room_name = f"{user.profile.id}-{profile.id}" if user.profile.id >= profile.id else f"{profile.id}-{user.profile.id}"
        try:
            chat = Chat.objects.get(name=room_name)
        except Chat.DoesNotExist:
            return JsonResponse (
                {"message": "Chat not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        messages = Message.objects.filter(
            Q(chat=chat, receiver=user.profile) | Q(chat=chat, sender=user.profile)
        ).order_by('-created_at')[start:start+30]
        if not messages.exists():
            return JsonResponse(
                {"message": "No more messages to load."},
                status=status.HTTP_204_NO_CONTENT
            )
        return JsonResponse(
            [{
                'id': message.id,
                'receiver': message.receiver.username,
                'sender': message.sender.username,
                'content': message.content,
                'created_at': message.created_at.isoformat(),
                'is_read': message.is_read
            } for message in messages][::-1],
            safe=False,
            status=status.HTTP_200_OK
        )
