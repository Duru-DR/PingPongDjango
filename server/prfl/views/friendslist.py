from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..utils                    import friendslist

class FriendsListView(generics.GenericAPIView):
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        friends_list = friendslist(user.profile)
        
        return JsonResponse(
            friends_list,
            safe=False, 
            status = status.HTTP_200_OK,
        )
        