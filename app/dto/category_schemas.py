from pydantic import BaseModel
from typing import Optional, List

class CategoryCreateRequest(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: int = 0

class CategoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    image_url: Optional[str]
    parent_id: Optional[int]
    sort_order: int
    is_active: bool

    model_config = {"from_attributes": True}

class CategoryTreeResponse(CategoryResponse):

    children: List["CategoryTreeResponse"] = []

CategoryTreeResponse.model_rebuild()
