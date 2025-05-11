from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..models                   import BlockedFriend

class BlockedFriendsView(generics.GenericAPIView):
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        profile = user.profile
        blockedfriends = BlockedFriend.objects.filter(blocker=profile)

        blockedfriends_data = blockedfriends.values(
            'blocked_friend__username', 
            'blocked_friend__is_online', 
            'blocked_friend__picture', 
            'blocked_friend__rank'
        )

        formatted_data = [
            {
                'username': item['blocked_friend__username'],
                'is_online': item['blocked_friend__is_online'],
                'picture': item['blocked_friend__picture'],
                'rank': item['blocked_friend__rank']
            }
            for item in blockedfriends_data
        ]

        return JsonResponse(
            formatted_data,
            safe=False, 
            status=status.HTTP_200_OK,
        )
