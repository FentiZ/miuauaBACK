from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List

from app.data.top_category import TopCategory
from app.dto.top_category_schemas import (
    TopCategoryCreateRequest,
    TopCategoryUpdateRequest,
    TopCategoryResponse,
    TopCategoryWithDownResponse,
)
from app.utils.helpers import slugify


class TopCategoryController:

    @staticmethod
    def list_all(db: Session) -> List[TopCategoryResponse]:
        items = (
            db.query(TopCategory)
            .filter(TopCategory.is_active == True)
            .order_by(TopCategory.sort_order)
            .all()
        )
        return [TopCategoryResponse.model_validate(i) for i in items]

    @staticmethod
    def list_with_down(db: Session) -> List[TopCategoryWithDownResponse]:
        """Возвращает TopCategory вместе с вложенными DownCategory."""
        items = (
            db.query(TopCategory)
            .filter(TopCategory.is_active == True)
            .order_by(TopCategory.sort_order)
            .all()
        )
        return [TopCategoryWithDownResponse.model_validate(i) for i in items]

    @staticmethod
    def get_by_slug(slug: str, db: Session) -> TopCategoryResponse:
        item = db.query(TopCategory).filter(TopCategory.slug == slug).first()
        if not item:
            raise HTTPException(status_code=404, detail="TopCategory не найдена")
        return TopCategoryResponse.model_validate(item)

    @staticmethod
    def create(payload: TopCategoryCreateRequest, db: Session) -> TopCategoryResponse:
        slug = payload.slug or slugify(payload.name)
        if db.query(TopCategory).filter(TopCategory.slug == slug).first():
            raise HTTPException(status_code=409, detail=f"TopCategory со slug '{slug}' уже существует")

        data = payload.model_dump()
        data["slug"] = slug
        item = TopCategory(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return TopCategoryResponse.model_validate(item)

    @staticmethod
    def update(item_id: int, payload: TopCategoryUpdateRequest, db: Session) -> TopCategoryResponse:
        item = db.query(TopCategory).filter(TopCategory.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="TopCategory не найдена")

        update_data = payload.model_dump(exclude_unset=True)
        if "slug" in update_data and update_data["slug"]:
            exists = db.query(TopCategory).filter(
                TopCategory.slug == update_data["slug"],
                TopCategory.id != item_id,
            ).first()
            if exists:
                raise HTTPException(status_code=409, detail="Такой slug уже занят")

        for field, value in update_data.items():
            setattr(item, field, value)

        db.commit()
        db.refresh(item)
        return TopCategoryResponse.model_validate(item)

    @staticmethod
    def delete(item_id: int, db: Session) -> dict:
        item = db.query(TopCategory).filter(TopCategory.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="TopCategory не найдена")
        db.delete(item)
        db.commit()
        return {"message": f"TopCategory {item_id} удалена", "success": True}
