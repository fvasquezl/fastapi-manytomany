from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.core import NotFoundError, get_db
from app.db.users import (
    User,
    UserCreate,
    UserUpdate,
    read_db_user,
    create_db_user,
    update_db_user,
    delete_db_user,
    read_db_posts_for_user,
)

from app.db.posts import Post


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


@router.get("/{item_id}/posts")
def read_item_automations(
    request: Request, item_id: int, db: Session = Depends(get_db)
) -> list[Post]:
    try:
        automations = read_db_posts_for_user(item_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return [Post(**automation.__dict__) for automation in automations]


@router.put("/{user_id}")
def update_user(
    request: Request, user_id: int, user: UserUpdate, db: Session = Depends(get_db)
) -> User:
    try:
        db_user = update_db_user(user_id, user, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return User(**db_user.__dict__)


@router.delete("/{user_id}")
def delete_user(request: Request, user_id: int, db: Session = Depends(get_db)) -> User:
    try:
        db_user = delete_db_user(user_id, db)
    except NotFoundError as e:
        raise HTTPException(status_code=404) from e
    return User(**db_user.__dict__)
