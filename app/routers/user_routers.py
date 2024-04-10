from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.models.user_model import UserDB
from app.schemas.user_schema import User, UserCreate


user_router = APIRouter()


def get_db(request: Request):
    return request.state.db


# Rutas para usuarios


@user_router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserDB(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@user_router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
