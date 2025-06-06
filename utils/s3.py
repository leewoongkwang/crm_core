import boto3
from django.conf import settings
import uuid

def upload_pdf_to_s3(file, user_id: int) -> str:
    s3 = boto3.client(
        's3',
        region_name=settings.AWS_S3_REGION_NAME  # ✔ region만 설정
    )

    filename = f"reports/{user_id}/{uuid.uuid4().hex}.pdf"
    s3.upload_fileobj(
        file,
        settings.AWS_STORAGE_BUCKET_NAME,
        filename,
        ExtraArgs={
            'ACL': 'public-read',
            'ContentType': 'application/pdf'
        }
    )

    return f"{settings.AWS_S3_BASE_URL}/{filename}"
