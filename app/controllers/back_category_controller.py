from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.data.back_category import BackCategory
from app.dto.back_category_schemas import (
    BackCategoryCreateRequest,
    BackCategoryUpdateRequest,
    BackCategoryResponse,
    BackCategoryTreeResponse,
)
from app.utils.helpers import slugify


class BackCategoryController:

    @staticmethod
    def _build_tree(
        categories: List[BackCategory],
        parent_id: Optional[int] = None,
    ) -> List[BackCategoryTreeResponse]:
        nodes = []
        for cat in [c for c in categories if c.parent_id == parent_id]:
            node = BackCategoryTreeResponse.model_validate(cat)
            node.children = BackCategoryController._build_tree(categories, cat.id)
            nodes.append(node)
        return sorted(nodes, key=lambda n: n.sort_order)

    @staticmethod
    def get_tree(db: Session) -> List[BackCategoryTreeResponse]:
        items = db.query(BackCategory).filter(BackCategory.is_active == True).all()
        return BackCategoryController._build_tree(items, None)

    @staticmethod
    def list_flat(db: Session) -> List[BackCategoryResponse]:
        items = (
            db.query(BackCategory)
            .filter(BackCategory.is_active == True)
            .order_by(BackCategory.sort_order)
            .all()
        )
        return [BackCategoryResponse.model_validate(i) for i in items]

    @staticmethod
    def get_by_slug(slug: str, db: Session) -> BackCategoryResponse:
        item = db.query(BackCategory).filter(BackCategory.slug == slug).first()
        if not item:
            raise HTTPException(status_code=404, detail="BackCategory не найдена")
        return BackCategoryResponse.model_validate(item)

    @staticmethod
    def create(payload: BackCategoryCreateRequest, db: Session) -> BackCategoryResponse:
        slug = payload.slug or slugify(payload.name)
        if db.query(BackCategory).filter(BackCategory.slug == slug).first():
            raise HTTPException(status_code=409, detail=f"BackCategory со slug '{slug}' уже существует")
        if payload.parent_id is not None:
            if not db.query(BackCategory).filter(BackCategory.id == payload.parent_id).first():
                raise HTTPException(status_code=404, detail="Родительская BackCategory не найдена")

        data = payload.model_dump()
        data["slug"] = slug
        item = BackCategory(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return BackCategoryResponse.model_validate(item)

    @staticmethod
    def update(item_id: int, payload: BackCategoryUpdateRequest, db: Session) -> BackCategoryResponse:
        item = db.query(BackCategory).filter(BackCategory.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="BackCategory не найдена")

        update_data = payload.model_dump(exclude_unset=True)
        if "slug" in update_data and update_data["slug"]:
            exists = db.query(BackCategory).filter(
                BackCategory.slug == update_data["slug"],
                BackCategory.id != item_id,
            ).first()
            if exists:
                raise HTTPException(status_code=409, detail="Такой slug уже занят")
        if update_data.get("parent_id") == item_id:
            raise HTTPException(status_code=400, detail="Категория не может быть родителем самой себе")

        for field, value in update_data.items():
            setattr(item, field, value)

        db.commit()
        db.refresh(item)
        return BackCategoryResponse.model_validate(item)

    @staticmethod
    def delete(item_id: int, db: Session) -> dict:
        item = db.query(BackCategory).filter(BackCategory.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="BackCategory не найдена")
        if item.children:
            raise HTTPException(status_code=400, detail="Сначала удалите дочерние пункты")
        db.delete(item)
        db.commit()
        return {"message": f"BackCategory {item_id} удалена", "success": True}
