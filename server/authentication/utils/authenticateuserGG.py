from django.contrib.auth        import get_user_model
from prfl.models                import Profile
from .random                    import random_passwd
from .print_color               import print_yellow
from minio                      import Minio
from django.conf                import settings
from django.core.files.base     import ContentFile
import requests
import io

User = get_user_model()

minio_client = Minio(
    "minio:9000",
    access_key=settings.AWS_ACCESS_KEY_ID,
    secret_key=settings.AWS_SECRET_ACCESS_KEY,
    secure=False,
)

def upload_image_to_minio(image_content, file_name, bucket_name):
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
        
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=file_name,
            data=io.BytesIO(image_content),
            length=len(image_content),
            content_type="image/jpeg",
        )
        return f"unsafe/{file_name}"
    except Exception as e:
        raise Exception(f"Failed to upload to MinIO: {e}")

def AuthenticateUserGG(request, data):
    email = data.get('email')
    user = User.objects.filter(email=email).first()

    if not user:
        username = data.get('name')
        first_name = data.get('given_name')
        last_name = data.get('family_name')
        image_url = data.get('picture')
        print_yellow(f'authenticateGG {image_url}')
        
        if User.objects.filter(username=username).exists():
            raise ValueError(f"The username '{username}' is already taken. Please use a different username.")

        response = requests.get(image_url)
        if response.status_code == 200:
            image_content = response.content
            file_name = f"{username}_picture.jpg"
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            
            minio_url = upload_image_to_minio(image_content, file_name, bucket_name)
        else:
            minio_url = None

        user = User.objects.create_user(
            username=username, 
            email=email, 
            first_name=first_name,
            last_name=last_name,
            password=random_passwd()
        )

        Profile.objects.create(
            user=user,
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            picture=minio_url,
        )

    return user.id
