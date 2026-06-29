from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional

from app.data.category import Category
from app.dto.category_schemas import (
    CategoryCreateRequest, CategoryUpdateRequest, CategoryResponse, CategoryTreeResponse,
)
from app.utils.helpers import slugify

class CategoryController:

    @staticmethod
    def _build_tree(categories: List[Category], parent_id: Optional[int] = None) -> List[CategoryTreeResponse]:
        nodes = []
        for cat in [c for c in categories if c.parent_id == parent_id]:
            node = CategoryTreeResponse.model_validate(cat)
            node.children = CategoryController._build_tree(categories, cat.id)
            nodes.append(node)
        return sorted(nodes, key=lambda n: n.sort_order)

    @staticmethod
    def get_tree(db: Session) -> List[CategoryTreeResponse]:

        categories = db.query(Category).filter(Category.is_active == True).all()
        return CategoryController._build_tree(categories, None)

    @staticmethod
    def list_flat(db: Session) -> List[CategoryResponse]:
        categories = db.query(Category).filter(Category.is_active == True).order_by(Category.sort_order).all()
        return [CategoryResponse.model_validate(c) for c in categories]

    @staticmethod
    def get_by_slug(slug: str, db: Session) -> CategoryResponse:
        category = db.query(Category).filter(Category.slug == slug).first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        return CategoryResponse.model_validate(category)

    @staticmethod
    def create(payload: CategoryCreateRequest, db: Session) -> CategoryResponse:
        slug = payload.slug or slugify(payload.name)
        if db.query(Category).filter(Category.slug == slug).first():
            raise HTTPException(status_code=409, detail=f"Категория со slug '{slug}' уже существует")
        if payload.parent_id is not None and not db.query(Category).filter(Category.id == payload.parent_id).first():
            raise HTTPException(status_code=404, detail="Родительская категория не найдена")

        data = payload.model_dump()
        data["slug"] = slug
        category = Category(**data)
        db.add(category)
        db.commit()
        db.refresh(category)
        return CategoryResponse.model_validate(category)

    @staticmethod
    def update(category_id: int, payload: CategoryUpdateRequest, db: Session) -> CategoryResponse:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")

        update_data = payload.model_dump(exclude_unset=True)
        if "slug" in update_data and update_data["slug"]:
            exists = db.query(Category).filter(Category.slug == update_data["slug"], Category.id != category_id).first()
            if exists:
                raise HTTPException(status_code=409, detail="Такой slug уже занят")
        if update_data.get("parent_id") == category_id:
            raise HTTPException(status_code=400, detail="Категория не может быть родителем самой себе")

        for field, value in update_data.items():
            setattr(category, field, value)

        db.commit()
        db.refresh(category)
        return CategoryResponse.model_validate(category)

    @staticmethod
    def delete(category_id: int, db: Session) -> dict:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Категория не найдена")
        if category.children:
            raise HTTPException(status_code=400, detail="Сначала удалите или переместите подкатегории")
        if category.products:
            raise HTTPException(status_code=400, detail="В категории есть товары — удаление запрещено")

        db.delete(category)
        db.commit()
        return {"message": f"Категория {category_id} удалена", "success": True}
