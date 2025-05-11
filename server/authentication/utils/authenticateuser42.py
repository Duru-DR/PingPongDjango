from django.contrib.auth    import authenticate, login
from django.contrib.auth    import get_user_model
from prfl.models            import Profile
from .random                import random_passwd
from .print_color           import print_yellow, print_green
from django.core.files.base import ContentFile
from minio                  import Minio
from django.conf            import settings
from .                      import upload_image_to_minio
import requests
import io

User = get_user_model()

def AuthenticateUser42(request, data):
    email = data.get('email')
    user = User.objects.filter(email=email).first()

    if not user:
        username = data.get('login')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        country = data.get('campus')[0].get('country')
        city = data.get('campus')[0].get('city')
        address = data.get('campus')[0].get('address')
        zip_code = data.get('campus')[0].get('zip')
        
        image_url = data.get('image', {}).get('versions', {}).get('small')
        print_yellow(f'authenticate42 {image_url}')

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
            country=country,
            city=city,
            address=address,
            zip_code=zip_code,
            picture=minio_url,
        )
    return user.id
    