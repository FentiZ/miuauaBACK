from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.data.brand import Brand
from app.dto.brand_schemas import BrandCreateRequest, BrandUpdateRequest, BrandResponse
from app.utils.helpers import slugify

class BrandController:

    @staticmethod
    def list_all(db: Session, only_active: bool = True) -> List[BrandResponse]:
        query = db.query(Brand)
        if only_active:
            query = query.filter(Brand.is_active == True)
        brands = query.order_by(Brand.name).all()
        return [BrandResponse.model_validate(b) for b in brands]

    @staticmethod
    def get_by_slug(slug: str, db: Session) -> BrandResponse:
        brand = db.query(Brand).filter(Brand.slug == slug).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Бренд не найден")
        return BrandResponse.model_validate(brand)

    @staticmethod
    def create(payload: BrandCreateRequest, db: Session) -> BrandResponse:
        slug = payload.slug or slugify(payload.name)
        if db.query(Brand).filter(Brand.slug == slug).first():
            raise HTTPException(status_code=409, detail=f"Бренд со slug '{slug}' уже существует")
        if db.query(Brand).filter(Brand.name == payload.name).first():
            raise HTTPException(status_code=409, detail=f"Бренд '{payload.name}' уже существует")

        data = payload.model_dump()
        data["slug"] = slug
        brand = Brand(**data)
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return BrandResponse.model_validate(brand)

    @staticmethod
    def update(brand_id: int, payload: BrandUpdateRequest, db: Session) -> BrandResponse:
        brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Бренд не найден")

        update_data = payload.model_dump(exclude_unset=True)
        if "slug" in update_data and update_data["slug"]:
            exists = db.query(Brand).filter(Brand.slug == update_data["slug"], Brand.id != brand_id).first()
            if exists:
                raise HTTPException(status_code=409, detail="Такой slug уже занят")

        for field, value in update_data.items():
            setattr(brand, field, value)

        db.commit()
        db.refresh(brand)
        return BrandResponse.model_validate(brand)

    @staticmethod
    def delete(brand_id: int, db: Session) -> dict:
        brand = db.query(Brand).filter(Brand.id == brand_id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Бренд не найден")
        if brand.products:
            raise HTTPException(status_code=400, detail="У бренда есть товары — удаление запрещено")

        db.delete(brand)
        db.commit()
        return {"message": f"Бренд {brand_id} удалён", "success": True}
