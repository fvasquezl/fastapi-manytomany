from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.core import NotFoundError, get_db
from app.db.roles import (
    Role,
    RoleCreate,
    RoleUpdate,
    read_db_role,
    create_db_role,
    update_db_role,
    delete_db_role,
    read_db_users_for_role,
)

from app.db.users import User


router = APIRouter(
    prefix="/roles",
)


@router.post("/")
def create_role(request: Request, role: RoleCreate, db: Session = Depends(get_db)) -> Role:
    db_role = create_db_role(role, db)
    return Role(**db_role.__dict__)


@router.get("/{role_id}", response_model=Role)
def read_role(request: Request, role_id: int, db: Session = Depends(get_db)) -> Role:
    try:
        db_role = read_db_role(role_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=400) from e
    return Role(**db_role.__dict__)


@router.get("/{item_id}/users")
def read_item_automations(
    request: Request, item_id: int, db: Session = Depends(get_db)
) -> list[User]:
    try:
        automations = read_db_users_for_role(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return [User(**automation.__dict__) for automation in automations]


@router.put("/{role_id}")
def update_role(
    request: Request, role_id: int, role: RoleUpdate, db: Session = Depends(get_db)
) -> Role:
    try:
        db_role = update_db_role(role_id, role, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Role(**db_role.__dict__)


@router.delete("/{role_id}")
def delete_role(request: Request, role_id: int, db: Session = Depends(get_db)) -> Role:
    try:
        db_role = delete_db_role(role_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Role(**db_role.__dict__)


# # Rutas para las etiquetas
# @router.post("/roles/", response_model=Role)
# def create_role(role: RoleCreate, db: Session = Depends(get_db)):
#     db_role = RoleDB(**role.model_dump())
#     db.add(db_role)
#     db.commit()
#     db.refresh(db_role)
#     return db_role


# @router.get("/roles/{role_id}", response_model=Role)
# def read_role(role_id: int, db: Session = Depends(get_db)):
#     role = db.query(RoleDB).filter(RoleDB.id == role_id).first()
#     if role is None:
#         raise HTTPException(status_code=404, detail="Role not found")
#     return role
