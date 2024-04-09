from pydantic import BaseModel, constr, validator
from typing import List, Optional
import re


class TagBase(BaseModel):
    nombre: str
    slug: Optional[str]

    @validator("slug", pre=True, always=True)
    def generate_slug(cls, v, values):
        if v:
            return v
        if "nombre" in values:
            return cls.slugify(values["nombre"])
        return None

    @staticmethod
    def slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True
