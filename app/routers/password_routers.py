from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.password_model import PasswordDB
from app.models.tag_model import TagDB
from app.schemas.password_schema import PasswordCreate, Password
from app.schemas.tag_schema import Tag

from typing import List

password_router = APIRouter()


def get_db(request: Request):
    return request.state.db


# Rutas para las contraseñas
@password_router.post("/passwords/", response_model=Password)
def create_password(
    password: PasswordCreate, tag_ids: List[int], db: Session = Depends(get_db)
):
    db_password = PasswordDB(**password.model_dump())

    for tag_id in tag_ids:
        tag = db.query(TagDB).filter(TagDB.id == tag_id).first()
        if tag is None:
            raise HTTPException(
                status_code=404, detail=f"Tag with id {tag_id} not found"
            )
        db_password.tags.append(tag)

    db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password


@password_router.get("/passwords/{password_id}", response_model=Password)
def read_password(password_id: int, db: Session = Depends(get_db)):
    password = db.query(PasswordDB).filter(PasswordDB.id == password_id).first()
    if password is None:
        raise HTTPException(status_code=404, detail="Password not found")
    return password


# Ruta para obtener los tags relacionados con un password
@password_router.get("/passwords/{password_id}/tags/", response_model=List[Tag])
def get_tags_for_password(password_id: int, db: Session = Depends(get_db)):
    password = db.query(PasswordDB).filter(PasswordDB.id == password_id).first()
    if password is None:
        raise HTTPException(status_code=404, detail="Password not found")
    return password.tags
