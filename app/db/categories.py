from datetime import datetime
from typing import Annotated, Optional, List
from pydantic import BaseModel, Field, validator
from .core import DBCategory, DBPost, NotFoundError
from sqlalchemy.orm import Session
import re


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    slug: Optional[str]

    @validator("slug", pre=True, always=True)
    def generate_slug(cls, v, values):
        if v:
            return v
        if "name" in values:
            return cls.slugify(values["name"])
        return None

    @staticmethod
    def slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text


class CategoryUpdate(CategoryBase):
    name: Optional[str] = None
    slug: Optional[str] = None


class Category(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


def read_db_category(category_id: int, session: Session) -> DBCategory:
    db_category = session.query(DBCategory).filter(DBCategory.id == category_id).first()
    if db_category is None:
        raise NotFoundError(f"category with id {category_id} not found.")
    return db_category


def read_db_posts_for_category(
    category_id: int, session: Session
) -> list[DBPost]:
    return session.query(DBPost).filter(DBPost.category_id == category_id).all()


def create_db_category(category: CategoryCreate, session: Session) -> DBCategory:
    db_category = DBCategory(**category.model_dump(exclude_none=True))
    session.add(db_category)
    session.commit()
    session.refresh(db_category)

    return db_category


def update_db_category(
    category_id: int, category: CategoryUpdate, session: Session
) -> DBCategory:
    db_category = read_db_category(category_id, session)
    for key, value in category.model_dump(exclude_none=True).items():
        setattr(db_category, key, value)
    session.commit()
    session.refresh(db_category)

    # get the posts
    # posts = read_db_posts_for_category(db_category.id, session)
    # run_posts(posts)

    return db_category


def delete_db_category(category_id: int, session: Session) -> DBCategory:
    db_category = read_db_category(category_id, session)
    session.delete(db_category)
    session.commit()
    return db_category
