from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from app.core.db import engine, SessionLocal
from app.schemas import User, UserCreate
import app.models as models


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]


@router.get('/users/{user_id}', response_model=User)
def read_user(user_id: int, db: SessionDep):
    user = db.scalars(select(models.User).where(
        models.User.id == user_id)).first()
    return user


@router.get('/users', response_model=User)
def read_user(uid: str, db: SessionDep):
    user = db.scalars(select(models.User).where(
        models.User.firebase_uid == uid)).first()

    if (user):
        return user
    else:
        raise HTTPException(
            status_code=404, detail='Associated user cannot be found.')


@router.post('/users/create', response_model=User)
def create_user(request: UserCreate, db: SessionDep):
    user = models.User(**request.model_dump())
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail='Firebase UID already exists.')

    return user
