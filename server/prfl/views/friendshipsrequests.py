from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..models                   import FriendRequest

class FriendshipsRequestsView(generics.GenericAPIView):
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        profile = user.profile
        friendshiprequests = FriendRequest.objects.filter(to_user=profile)

        friendshiprequests_data = friendshiprequests.values(
            'from_user__username', 
            'from_user__is_online', 
            'from_user__picture', 
            'from_user__rank'
        )
        formatted_data = [
            {
                'username': item['from_user__username'],
                'is_online': item['from_user__is_online'],
                'picture': item['from_user__picture'],
                'rank': item['from_user__rank']
            }
            for item in friendshiprequests_data
        ]

        return JsonResponse(
            formatted_data,
            safe=False, 
            status=status.HTTP_200_OK,
        )