from pydantic import BaseModel
from typing import Optional, List


class BackCategoryCreateRequest(BaseModel):
    name: str
    slug: Optional[str] = None
    description: Optional[str] = None
    icon_name: Optional[str] = None
    icon_url: Optional[str] = None
    sort_order: int = 0
    category_id: Optional[int] = None
    parent_id: Optional[int] = None


class BackCategoryUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    icon_name: Optional[str] = None
    icon_url: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None
    category_id: Optional[int] = None
    parent_id: Optional[int] = None


class BackCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    icon_name: Optional[str]
    icon_url: Optional[str]
    sort_order: int
    is_active: bool
    category_id: Optional[int]
    parent_id: Optional[int]

    model_config = {"from_attributes": True}


class BackCategoryTreeResponse(BackCategoryResponse):
    """BackCategory с вложенными дочерними пунктами (подменю)."""
    children: List["BackCategoryTreeResponse"] = []


BackCategoryTreeResponse.model_rebuild()
