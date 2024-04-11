from typing import Optional
from pydantic import BaseModel, validator
from .core import DBTag, DBTag, DBPassword, NotFoundError
from sqlalchemy.orm import Session
import re


class TagBase(BaseModel):
    name: str
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


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    pass


class Tag(TagBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


def read_db_tag(tag_id: int, session: Session) -> DBTag:
    db_tag = session.query(DBTag).filter(DBTag.id == tag_id).first()
    if db_tag is None:
        raise NotFoundError(f"tag with id {tag_id} not found.")
    return db_tag


def read_db_passwords_for_tag(tag_id: int, session: Session) -> list[DBPassword]:
    return session.query(DBPassword).filter(DBPassword.tag_id == tag_id).all()


def create_db_tag(tag: TagCreate, session: Session) -> DBTag:
    db_tag = DBTag(**tag.model_dump(exclude_none=True))
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)

    return db_tag


def update_db_tag(tag_id: int, tag: TagUpdate, session: Session) -> DBTag:
    db_tag = read_db_tag(tag_id, session)
    for key, value in tag.model_dump(exclude_none=True).items():
        setattr(db_tag, key, value)
    session.commit()
    session.refresh(db_tag)

    # get the passwords
    # passwords = read_db_passwords_for_tag(db_tag.id, session)
    # run_passwords(passwords)

    return db_tag


def delete_db_tag(tag_id: int, session: Session) -> DBTag:
    db_tag = read_db_tag(tag_id, session)
    session.delete(db_tag)
    session.commit()
    return db_tag
