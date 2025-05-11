import boto3
from django.conf import settings

def generate_presigned_url(object_key):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name='eu-south-2'
    )

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': object_key},
            ExpiresIn=259200
        )
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        return None

    return response
