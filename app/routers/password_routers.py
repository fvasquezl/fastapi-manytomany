from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.db.core import get_db, NotFoundError
from app.db.passwords import (
    Password,
    PasswordCreate,
    PasswordUpdate,
    create_db_password,
    delete_db_password,
    read_db_password,
    update_db_password,
)

from typing import List

router = APIRouter(
    prefix="/passwords",
)


# Rutas para las passwords
@router.post("/{user_id}/{category_id}/tags")
def create_password(
    category_id: int,
    user_id: int,
    password: PasswordCreate,
    tags: List[int] = Body(...),
    db: Session = Depends(get_db),
) -> Password:
    db_password = create_db_password(category_id, user_id, password, tags, db)
    return Password(**db_password.__dict__)


@router.get("/{password_id}")
def read_password(
    request: Request, password_id: int, db: Session = Depends(get_db)
) -> Password:
    try:
        db_password = read_db_password(password_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Password(**db_password.__dict__)


@router.put("/{password_id}")
def update_password(
    password_id: int,
    password: PasswordUpdate,
    db: Session = Depends(get_db),
) -> Password:
    try:
        db_password = update_db_password(password_id, password, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Password(**db_password.__dict__)


@router.delete("/{password_id}")
def delete_item(password_id: int, db: Session = Depends(get_db)) -> Password:
    try:
        db_password = delete_db_password(password_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return Password(**db_password.__dict__)


# @router.post("/passwords/", response_model=Password)
# def create_password(
#     password: PasswordCreate, tag_ids: List[int], db: Session = Depends(get_db)
# ):
#     db_password = Password(**password.model_dump())

#     for tag_id in tag_ids:
#         tag = db.query(TagDB).filter(TagDB.id == tag_id).first()
#         if tag is None:
#             raise HTTPException(
#                 status_code=404, detail=f"Tag with id {tag_id} not found"
#             )
#         db_password.tags.append(tag)

#     db.add(db_password)
#     db.commit()
#     db.refresh(db_password)
#     return db_password


# # Ruta para obtener los tags relacionados con un password
# @router.get("/passwords/{password_id}/tags/", response_model=List[Tag])
# def get_tags_for_password(password_id: int, db: Session = Depends(get_db)):
#     password = db.query(Password).filter(Password.id == password_id).first()
#     if password is None:
#         raise HTTPException(status_code=404, detail="Password not found")
#     return password.tags
