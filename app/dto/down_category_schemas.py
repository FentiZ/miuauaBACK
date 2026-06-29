from pydantic import BaseModel
from typing import Optional


class DownCategoryCreateRequest(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: int = 0
    top_category_id: Optional[int] = None
    category_id: Optional[int] = None


class DownCategoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    top_category_id: Optional[int] = None
    category_id: Optional[int] = None


class DownCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    image_url: Optional[str]
    sort_order: int
    is_active: bool
    top_category_id: Optional[int]
    category_id: Optional[int]

    model_config = {"from_attributes": True}
