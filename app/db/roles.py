from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .core import DBRole, DBUser, NotFoundError
from sqlalchemy.orm import Session


class RoleBase(BaseModel):
    name: str
    slug: Optional[str]

class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    name: Optional[str] = None
    slug: Optional[str] = None
    pass


class Role(RoleBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


def read_db_role(role_id: int, session: Session) -> DBRole:
    db_role = session.query(DBRole).filter(DBRole.id == role_id).first()
    if db_role is None:
        raise NotFoundError(f"role with id {role_id} not found.")
    return db_role


def read_db_users_for_role(role_id: int, session: Session) -> list[DBUser]:
    return session.query(DBUser).filter(DBUser.role_id == role_id).all()


def create_db_role(role: RoleCreate, session: Session) -> DBRole:
    db_role = DBRole(**role.model_dump(exclude_none=True))
    session.add(db_role)
    session.commit()
    session.refresh(db_role)

    return db_role


def update_db_role(role_id: int, role: RoleUpdate, session: Session) -> DBRole:
    db_role = read_db_role(role_id, session)
    for key, value in role.model_dump(exclude_none=True).items():
        setattr(db_role, key, value)
    session.commit()
    session.refresh(db_role)

    # get the users
    # users = read_db_users_for_role(db_role.id, session)
    # run_users(users)

    return db_role


def delete_db_role(role_id: int, session: Session) -> DBRole:
    db_role = read_db_role(role_id, session)
    session.delete(db_role)
    session.commit()
    return db_role
