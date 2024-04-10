from pydantic import BaseModel, constr, validator
from typing import List, Optional
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


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
