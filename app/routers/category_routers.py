from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.category_model import CategoryDB
from app.schemas.category_schema import Category, CategoryCreate

from typing import List

category_router = APIRouter()


def get_db(request: Request):
    return request.state.db


# Rutas para las etiquetas
@category_router.post("/category/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = CategoryDB(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@category_router.get("/category/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryDB).filter(CategoryDB.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
