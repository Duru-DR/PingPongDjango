from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from authentication.utils import Authenticate
from ..models import Profile
from ..utils import generate_presigned_url

class CustomizePicsView(generics.GenericAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        print("Request Headers:")
        for header, value in request.headers.items():
            print(f"{header}: {value}")
        profile = user.profile
        print("^^^^^^^^^^^^^^^^^^^")
        picture = request.FILES.get('picture')
        # background_picture = request.FILES.get('background_picture')
        print(picture)
        # print(background_picture)
        if picture:
            profile.picture = picture

        # if background_picture:
        #     profile.background_picture = background_picture
        a = 'profile_pictures/' + str(picture)
        profile.save()
        response_data = {
            "message": "Profile pictures updated",
            "picture_url": generate_presigned_url(a),
            "background_picture_url": profile.background_picture.url if profile.background_picture else None,
        }
        return JsonResponse(response_data, status=status.HTTP_200_OK)
