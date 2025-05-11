from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..models                   import FriendRequest

class RequestedFriendshipsView(generics.GenericAPIView):
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        profile = user.profile
        requestedfriendships = FriendRequest.objects.filter(from_user=profile)

        requestedfriendships_data = requestedfriendships.values(
            'to_user__username', 
            'to_user__is_online', 
            'to_user__picture', 
            'to_user__rank'
        )
        formatted_data = [
            {
                'username': item['to_user__username'],
                'is_online': item['to_user__is_online'],
                'picture': item['to_user__picture'],
                'rank': item['to_user__rank']
            }
            for item in requestedfriendships_data
        ]

        return JsonResponse(
            formatted_data,
            safe=False, 
            status=status.HTTP_200_OK,
        )