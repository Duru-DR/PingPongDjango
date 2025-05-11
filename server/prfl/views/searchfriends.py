from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..models                   import Friend
from ..utils                    import friendslist

class SearchFriendsView(generics.GenericAPIView):
    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        prefix = request.data.get('prefix')
        friends_data = friendslist(user.profile, prefix=prefix)
        return JsonResponse(
            friends_data[:20],
            safe=False,
            status=status.HTTP_200_OK
        )