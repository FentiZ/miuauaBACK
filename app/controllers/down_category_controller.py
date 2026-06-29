from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.data.down_category import DownCategory
from app.dto.down_category_schemas import (
    DownCategoryCreateRequest,
    DownCategoryUpdateRequest,
    DownCategoryResponse,
)
from app.utils.helpers import slugify


class DownCategoryController:

    @staticmethod
    def list_all(db: Session, top_category_id: Optional[int] = None) -> List[DownCategoryResponse]:
        """
        Возвращает плоский список DownCategory.
        Если передан top_category_id — фильтрует по нему
        (лента для конкретной вкладки TopCategory).
        """
        q = db.query(DownCategory).filter(DownCategory.is_active == True)
        if top_category_id is not None:
            q = q.filter(DownCategory.top_category_id == top_category_id)
        items = q.order_by(DownCategory.sort_order).all()
        return [DownCategoryResponse.model_validate(i) for i in items]

    @staticmethod
    def get_by_slug(slug: str, db: Session) -> DownCategoryResponse:
        item = db.query(DownCategory).filter(DownCategory.slug == slug).first()
        if not item:
            raise HTTPException(status_code=404, detail="DownCategory не найдена")
        return DownCategoryResponse.model_validate(item)

    @staticmethod
    def create(payload: DownCategoryCreateRequest, db: Session) -> DownCategoryResponse:
        slug = payload.slug or slugify(payload.name)
        if db.query(DownCategory).filter(DownCategory.slug == slug).first():
            raise HTTPException(status_code=409, detail=f"DownCategory со slug '{slug}' уже существует")

        data = payload.model_dump()
        data["slug"] = slug
        item = DownCategory(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return DownCategoryResponse.model_validate(item)

    @staticmethod
    def update(item_id: int, payload: DownCategoryUpdateRequest, db: Session) -> DownCategoryResponse:
        item = db.query(DownCategory).filter(DownCategory.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="DownCategory не найдена")

        update_data = payload.model_dump(exclude_unset=True)
        if "slug" in update_data and update_data["slug"]:
            exists = db.query(DownCategory).filter(
                DownCategory.slug == update_data["slug"],
                DownCategory.id != item_id,
            ).first()
            if exists:
                raise HTTPException(status_code=409, detail="Такой slug уже занят")

        for field, value in update_data.items():
            setattr(item, field, value)

        db.commit()
        db.refresh(item)
        return DownCategoryResponse.model_validate(item)

    @staticmethod
    def delete(item_id: int, db: Session) -> dict:
        item = db.query(DownCategory).filter(DownCategory.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="DownCategory не найдена")
        db.delete(item)
        db.commit()
        return {"message": f"DownCategory {item_id} удалена", "success": True}
