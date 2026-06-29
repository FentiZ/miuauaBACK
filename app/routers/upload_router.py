from fastapi import APIRouter, Depends, UploadFile, File, Query
from typing import Literal

from app.data.user import User
from app.middleware.auth import require_admin
from app.utils.s3 import upload_image

router = APIRouter(prefix="/upload", tags=["Upload"])

class ImageUploadResponse:
    def __init__(self, url: str):
        self.url = url

@router.post("/image", summary="Загрузить изображение в S3")
async def upload_image_endpoint(
    file: UploadFile = File(..., description="Изображение (jpg/png/webp/gif, макс. 10 MB)"),
    folder: Literal["products", "banners", "brands", "categories"] = Query(
        default="products",
        description="Папка в S3-бакете",
    ),
    _admin: User = Depends(require_admin),
):

    url = await upload_image(file, folder=folder)
    return {"url": url}
