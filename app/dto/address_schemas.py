from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AddressCreateRequest(BaseModel):
    full_name: str
    phone: str
    city: str
    region: Optional[str] = None
    street: str
    house: str
    apartment: Optional[str] = None
    postal_code: Optional[str] = None
    is_default: bool = False

class AddressUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    street: Optional[str] = None
    house: Optional[str] = None
    apartment: Optional[str] = None
    postal_code: Optional[str] = None
    is_default: Optional[bool] = None

class AddressResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    city: str
    region: Optional[str]
    street: str
    house: str
    apartment: Optional[str]
    postal_code: Optional[str]
    is_default: bool
    created_at: datetime

    model_config = {"from_attributes": True}
