from typing import Union, Annotated
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from . import schemas
from . import models
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .db import engine, SessionLocal

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()

SessionDep = Annotated[Session, Depends(get_db)]

app = FastAPI()

@app.get('/')
def read_root():
    return {}
    
@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: SessionDep):
    user = db.scalars(select(models.User).where(models.User.id == user_id)).first()
    return user

@app.post('/users/create', response_model=schemas.User)
def create_user(request: schemas.UserCreate, db: SessionDep):
    user = models.User(**request.model_dump())
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail='Firebase UID already exists.')
    
    return user