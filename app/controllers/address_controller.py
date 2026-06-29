from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.data.address import Address
from app.data.user import User
from app.dto.address_schemas import AddressCreateRequest, AddressUpdateRequest, AddressResponse

class AddressController:

    @staticmethod
    def list_my(owner: User, db: Session) -> List[AddressResponse]:
        items = db.query(Address).filter(Address.user_id == owner.id).order_by(Address.is_default.desc(), Address.id.desc()).all()
        return [AddressResponse.model_validate(a) for a in items]

    @staticmethod
    def create(payload: AddressCreateRequest, owner: User, db: Session) -> AddressResponse:
        if payload.is_default:
            db.query(Address).filter(Address.user_id == owner.id).update({"is_default": False})

        address = Address(**payload.model_dump(), user_id=owner.id)
        db.add(address)
        db.commit()
        db.refresh(address)
        return AddressResponse.model_validate(address)

    @staticmethod
    def update(address_id: int, payload: AddressUpdateRequest, owner: User, db: Session) -> AddressResponse:
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Адрес не найден")
        if address.user_id != owner.id:
            raise HTTPException(status_code=403, detail="Нет прав на редактирование этого адреса")

        update_data = payload.model_dump(exclude_unset=True)
        if update_data.get("is_default"):
            db.query(Address).filter(Address.user_id == owner.id).update({"is_default": False})

        for field, value in update_data.items():
            setattr(address, field, value)

        db.commit()
        db.refresh(address)
        return AddressResponse.model_validate(address)

    @staticmethod
    def delete(address_id: int, owner: User, db: Session) -> dict:
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Адрес не найден")
        if address.user_id != owner.id:
            raise HTTPException(status_code=403, detail="Нет прав на удаление этого адреса")

        db.delete(address)
        db.commit()
        return {"message": "Адрес удалён", "success": True}
