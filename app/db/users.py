from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .core import DBUser, DBPost, NotFoundError
from sqlalchemy.orm import Session


class UserBase(BaseModel):
    name: str
    email: str
    full_name: str | None = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None


class User(UserBase):
    id: int
    disabled: bool | None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


def read_db_user(user_id: int, session: Session) -> DBUser:
    db_user = session.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise NotFoundError(f"user with id {user_id} not found.")
    return db_user


def read_db_posts_for_user(user_id: int, session: Session) -> list[DBPost]:
    return session.query(DBPost).filter(DBPost.user_id == user_id).all()


def create_db_user(user: UserCreate, session: Session) -> DBUser:
    db_user = DBUser(**user.model_dump(exclude_none=True))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def update_db_user(user_id: int, user: UserUpdate, session: Session) -> DBUser:
    db_user = read_db_user(user_id, session)
    for key, value in user.model_dump(exclude_none=True).items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)

    # get the posts
    # posts = read_db_posts_for_user(db_user.id, session)
    # run_posts(posts)

    return db_user


def delete_db_user(user_id: int, session: Session) -> DBUser:
    db_user = read_db_user(user_id, session)
    session.delete(db_user)
    session.commit()
    return db_user
