from typing import Union, Annotated
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi import Depends
import firebase_admin.auth
from . import schemas
from . import models
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .db import engine, SessionLocal
# from .fb import test_send
from .ride_handler import RideService
from firebase_admin import initialize_app, auth, credentials

# should use the recommended way of utilizing the GOOGLE_APPLICATION_CREDENTIALS environment variable
cred = firebase_admin.credentials.Certificate(
    'C:\\Users\\jhend\\keys\\aadd-be709-firebase-adminsdk-ouy5k-f31c82021f.json')
app = firebase_admin.initialize_app(cred)

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]

ride_service = RideService()

app = FastAPI()


@app.get('/')
def read_root():
    return {}


@app.get('/msgtest')
def msg_test():
    print('attempting test send')
    test_send()
    return {}


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: SessionDep):
    user = db.scalars(select(models.User).where(
        models.User.id == user_id)).first()
    return user


@app.get('/users', response_model=schemas.User)
def read_user(uid: str, db: SessionDep):
    user = db.scalars(select(models.User).where(
        models.User.firebase_uid == uid)).first()

    if (user):
        return user
    else:
        raise HTTPException(
            status_code=404, detail='Associated user cannot be found.')


@app.post('/users/create', response_model=schemas.User)
def create_user(request: schemas.UserCreate, db: SessionDep):
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


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await ride_service.connect(websocket)

    try:
        decoded_token = auth.verify_id_token(
            websocket.headers['authorization'])
    except auth.InvalidIdTokenError:
        await websocket.close()
        return

    async for data in websocket.iter_json():
        ride_service.process_message(data, websocket)
        print(f'Message received was: {data}')

    # WebSocketDisconnect raised
    ride_service.disconnect(websocket)
