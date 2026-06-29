from pydantic import BaseModel
from typing import Optional

class StoreCreateRequest(BaseModel):
    city: str
    address: str
    phone: Optional[str] = None
    working_hours: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class StoreUpdateRequest(BaseModel):
    city: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    working_hours: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_active: Optional[bool] = None

class StoreResponse(BaseModel):
    id: int
    city: str
    address: str
    phone: Optional[str]
    working_hours: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    is_active: bool

    model_config = {"from_attributes": True}
