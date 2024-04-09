from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.tag import TagDB
from app.schemas.tag import Tag, TagCreate

from typing import List

tag_router = APIRouter()


def get_db(request: Request):
    return request.state.db


# Rutas para las etiquetas
@tag_router.post("/tags/", response_model=Tag)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    db_tag = TagDB(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@tag_router.get("/tags/{tag_id}", response_model=Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(TagDB).filter(TagDB.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag
