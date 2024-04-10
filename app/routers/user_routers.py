from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.core import NotFoundError, get_db
from app.db.users import (
    User,
    UserCreate,
    # UserUpdate,
    read_db_user,
    create_db_user,
    # update_db_user,
    delete_db_user,
    read_db_passwords_for_user,
)

router = APIRouter(
    prefix="/users",
)


# Rutas para usuarios


@router.post("/")
def create_user(
    request: Request, user: UserCreate, db: Session = Depends(get_db)
) -> User:
    db_user = create_db_user(user, db)
    return User(**db_user.__dict__)


@router.get("/{user_id}", response_model=User)
def read_user(request: Request, user_id: int, db: Session = Depends(get_db)) -> User:
    try:
        db_user = read_db_user(user_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=400) from e
    return User(**db_user.__dict__)
