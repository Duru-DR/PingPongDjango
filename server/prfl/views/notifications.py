from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..models                   import Profile, Notification
from ..serializers              import NotificationSerializer

class Notifications(generics.GenericAPIView):
    serializer_class = NotificationSerializer

    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        start = int(request.data.get('start', 0))
        notifications = Notification.objects.filter(profile=user.profile).order_by('-created_at')[start:start+10]
        serializer = NotificationSerializer(notifications, many=True)
        return JsonResponse(
            serializer.data, 
            safe = False,
            status = status.HTTP_200_OK
        )
