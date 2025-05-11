from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate
from ..serializers              import StatisticsSerializer
from ..models                   import Friend, Profile

class StatisticsView(generics.GenericAPIView):
    serializer_class = StatisticsSerializer
    
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        serializer = self.serializer_class(user.profile)
        return JsonResponse(
            serializer.data,
            status = status.HTTP_200_OK
        )
