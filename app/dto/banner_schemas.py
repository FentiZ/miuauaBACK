from pydantic import BaseModel
from typing import Optional

class BannerCreateRequest(BaseModel):
    title: Optional[str] = None
    image_url: str
    link_url: Optional[str] = None
    sort_order: int = 0

class BannerUpdateRequest(BaseModel):
    title: Optional[str] = None
    image_url: Optional[str] = None
    link_url: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None

class BannerResponse(BaseModel):
    id: int
    title: Optional[str]
    image_url: str
    link_url: Optional[str]
    sort_order: int
    is_active: bool

    model_config = {"from_attributes": True}

class CityResponse(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}
