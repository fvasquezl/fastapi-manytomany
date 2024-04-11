from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from .core import DBPassword, NotFoundError
from .users import read_db_user
from .categories import read_db_category


class PasswordBase(BaseModel):
    name: str
    description: str


class PasswordCreate(PasswordBase):
    slug: str


class PasswordUpdate(BaseModel):
    name: Optional[int] = None
    description: Optional[str] = None


class Password(PasswordBase):
    id: int
    category_id: int
    user_id: int

    class Config:
        from_attributes = True


def read_db_password(password_id: int, session: Session) -> DBPassword:
    db_password = session.query(DBPassword).filter(DBPassword.id == password_id).first()
    if db_password is None:
        raise NotFoundError(f"Password with id {password_id} not found.")
    return db_password


def create_db_password(
    category_id: int, user_id: int, password: PasswordCreate, session: Session
) -> DBPassword:
    user = read_db_user(user_id, session)
    category = read_db_category(category_id, session)
    db_password = DBPassword(**password.model_dump())
    db_password.user_id = user.id
    db_password.category_id = category.id
    session.add(db_password)
    session.commit()
    session.refresh(db_password)
    return db_password


def update_db_password(
    password_id: int, password: PasswordUpdate, session: Session
) -> DBPassword:
    db_password = read_db_password(password_id, session)
    for key, value in password.model_dump(exclude_none=True).items():
        setattr(db_password, key, value)
    session.commit()
    session.refresh(db_password)
    return db_password


def delete_db_password(password_id: int, session: Session) -> DBPassword:
    db_password = read_db_password(password_id, session)
    session.delete(db_password)
    session.commit()
    return db_password
