from django.contrib.auth    import authenticate
from django.http            import JsonResponse, HttpResponse
from rest_framework         import generics, status
from django.conf            import settings
from ..utils                import createJWTToken, JWTsGenerator, print_green, print_red
from ..serializers          import CustomUserSerializer
from ..models               import CustomUser
from django.core.cache      import cache

class SignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return JsonResponse(
            {"message": "User Created Successfully"},
            status=status.HTTP_201_CREATED
        )
