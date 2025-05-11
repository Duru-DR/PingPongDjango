from rest_framework         import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.http            import JsonResponse
from authentication.utils   import Authenticate, print_green, print_yellow, print_red
from ..models               import Profile
from ..utils                import generate_presigned_url
from ..serializers          import ProfileImageUploadSerializer, ProfileBackgroundUploadSerializer
from rest_framework         import serializers
from minio                  import Minio
from django.conf            import settings

minio_client = Minio(
    "minio:9000",
    access_key=settings.AWS_ACCESS_KEY_ID,
    secret_key=settings.AWS_SECRET_ACCESS_KEY,
    secure=False,
)

def upload_to_minio(file, file_name, file_size, content_type, bucket_name):
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)

        minio_client.put_object(
            bucket_name,
            file_name,
            file,
            length=file_size,
            content_type=content_type,
        )

        return f"unsafe/{file_name}"
    except Exception as e:
        raise serializers.ValidationError(f"Failed to upload to MinIO: {e}")    

class ProfileImageUploadView(generics.GenericAPIView):
    serializer_class = ProfileImageUploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        print_yellow(f'request data: {request.data}')
        profile = user.profile
        data_key = 'picture' 
        upload_data = {data_key: request.FILES.get(data_key)}

        serializer = self.serializer_class(profile, data=upload_data, partial=True)

        if serializer.is_valid():
            file = serializer.validated_data[data_key]
            file_content = file.file
            file_name = f'picture_{profile.username}_{file.name}'
            file_size = file.size
            content_type = file.content_type
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME

            try:
                minio_url = upload_to_minio(
                    file_content,
                    file_name,
                    file_size,
                    content_type,
                    bucket_name
                )
                setattr(profile, data_key, minio_url)
                profile.save()

                return JsonResponse(
                    {'message': 'Image uploaded successfully', 'data': serializer.data},
                    status=status.HTTP_200_OK
                )
            except serializers.ValidationError as e:
                print_red(f"MinIO upload error: {e}")
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            print_red(f'serializer errors: {serializer.errors}')
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileBackgroundUploadView(generics.GenericAPIView):
    serializer_class = ProfileBackgroundUploadSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        print_yellow(f'request data: {request.data}')
        profile = user.profile
        data_key = 'background_picture' 
        upload_data = {data_key: request.FILES.get(data_key)}

        serializer = self.serializer_class(profile, data=upload_data, partial=True)

        if serializer.is_valid():
            file = serializer.validated_data[data_key]
            file_content = file.file
            file_name = f'background_{profile.username}_{file.name}'
            file_size = file.size
            content_type = file.content_type
            bucket_name=settings.AWS_STORAGE_BUCKET_NAME

            try:
                minio_url = upload_to_minio(
                    file_content,
                    file_name,
                    file_size,
                    content_type,
                    bucket_name
                )
                setattr(profile, data_key, minio_url)
                profile.save()

                return JsonResponse(
                    {'message': 'Image uploaded successfully', 'data': serializer.data},
                    status=status.HTTP_200_OK
                )
            except serializers.ValidationError as e:
                print_red(f"MinIO upload error: {e}")
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            print_red(f'serializer errors: {serializer.errors}')
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
