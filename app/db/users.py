import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from .core import DBUser, DBPassword, NotFoundError
from sqlalchemy.orm import Session
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


def read_db_user(user_id: int, session: Session) -> DBUser:
    db_user = session.query(DBUser).filter(DBUser.id == user_id).first()
    if db_user is None:
        raise NotFoundError(f"user with id {user_id} not found.")
    return db_user


def read_db_passwords_for_user(user_id: int, session: Session) -> list[DBPassword]:
    return session.query(DBPassword).filter(DBPassword.user_id == user_id).all()


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

    # get the passwords
    # passwords = read_db_passwords_for_user(db_user.id, session)
    # run_passwords(passwords)

    return db_user


def delete_db_user(user_id: int, session: Session) -> DBUser:
    db_user = read_db_user(user_id, session)
    session.delete(db_user)
    session.commit()
    return db_user
