import os
import uuid
import mimetypes
from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile, status

from dotenv import load_dotenv

load_dotenv()

_AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
_AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
_AWS_REGION            = os.getenv("AWS_REGION", "eu-central-1")
_S3_BUCKET             = os.getenv("AWS_S3_BUCKET", "")
_S3_PUBLIC_URL         = os.getenv("AWS_S3_PUBLIC_URL", "").rstrip("/")

_ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
_MAX_SIZE_BYTES = 10 * 1024 * 1024

def _s3_client():

    if not _AWS_ACCESS_KEY_ID or not _AWS_SECRET_ACCESS_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="S3 не настроен: AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY отсутствуют",
        )
    return boto3.client(
        "s3",
        region_name=_AWS_REGION,
        aws_access_key_id=_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=_AWS_SECRET_ACCESS_KEY,
    )

async def upload_image(file: UploadFile, folder: str = "products") -> str:

    content_type = file.content_type or ""
    if content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Неподдерживаемый тип файла: {content_type}. Разрешено: {_ALLOWED_CONTENT_TYPES}",
        )

    contents = await file.read()
    if len(contents) > _MAX_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Файл слишком большой. Максимум: {_MAX_SIZE_BYTES // (1024 * 1024)} MB",
        )

    ext = Path(file.filename or "image.jpg").suffix.lower() or ".jpg"
    key = f"{folder}/{uuid.uuid4().hex}{ext}"

    try:
        client = _s3_client()
        client.put_object(
            Bucket=_S3_BUCKET,
            Key=key,
            Body=contents,
            ContentType=content_type,

        )
    except ClientError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Ошибка S3: {e.response['Error']['Message']}",
        )

    return f"{_S3_PUBLIC_URL}/{key}"

def delete_image(url: str) -> None:

    if not url.startswith(_S3_PUBLIC_URL):
        return
    key = url.removeprefix(_S3_PUBLIC_URL + "/")
    try:
        client = _s3_client()
        client.delete_object(Bucket=_S3_BUCKET, Key=key)
    except ClientError:
        pass
