from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate, print_green
from ..serializers              import PersonalDataSerializer

class PersonalDataView(generics.GenericAPIView):
    serializer_class = PersonalDataSerializer

    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.serializer_class(user.profile)
        print_green(f'dtaa: {serializer.data}')
        return JsonResponse(
            serializer.data,
            status = status.HTTP_200_OK
        )
