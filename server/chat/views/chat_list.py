from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..models                    import Chat
from django.utils               import timezone
from datetime                   import timedelta
from django.db.models           import Q

class ChatsView(generics.GenericAPIView):
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        chats = Chat.objects.filter(
            Q(user1=user.profile) | Q(user2=user.profile)
        )
        chats_data = []
        for chat in chats:
            other = chat.user2 if chat.user1 == user.profile else chat.user1
            
            last_message = chat.messages.order_by('-created_at').first()
            unread_messages = chat.messages.filter(receiver=user.profile, is_read=False).count()
            time_difference = None
            last_message_time = None
            if last_message:
                time_difference = timezone.now() - last_message.created_at
                last_message_time = last_message.created_at
            chats_data.append({
                "username": other.username,
                "picture": other.picture if other.picture else None,
                "rank": other.rank,
                "last_message_content": last_message.content if last_message else None,
                "is_online": other.is_online,
                "unread_messages": unread_messages,
                "last_message_time": last_message_time,
                "last_message_time_diff": str(time_difference) if time_difference else None,
            })
        return JsonResponse(
            chats_data,
            safe = False,
            status = status.HTTP_200_OK,
        )
# pic
# time
