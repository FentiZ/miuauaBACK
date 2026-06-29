from pydantic import BaseModel
from typing import Optional

class BrandCreateRequest(BaseModel):
    name: str
    slug: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None

class BrandUpdateRequest(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    logo_url: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class BrandResponse(BaseModel):
    id: int
    name: str
    slug: str
    logo_url: Optional[str]
    description: Optional[str]
    is_active: bool

    model_config = {"from_attributes": True}
