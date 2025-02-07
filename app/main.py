from fastapi import FastAPI
from fastapi import WebSocket
from firebase_admin import initialize_app, auth, credentials
from app.core.db import engine
import app.routers as routers
from app.routers.user import router
from app.models import Base
# from app.routers.user import router as UserRouter
from app.services.ride.ride_handler import RideService


# should use the recommended way of utilizing the GOOGLE_APPLICATION_CREDENTIALS environment variable
cred = credentials.Certificate(
    'C:\\Users\\jhend\\keys\\aadd-be709-firebase-adminsdk-ouy5k-f31c82021f.json')
fb_app = initialize_app(cred)

# models.Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(engine)

ride_service = RideService()

fapi_app = FastAPI()
fapi_app.include_router(routers.user.router)


@fapi_app.get('/')
def read_root():
    return {}


@fapi_app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await ride_service.connect(websocket)

    try:
        decoded_token = auth.verify_id_token(
            websocket.headers['authorization'])
    except auth.InvalidIdTokenError:
        print("Invalid user token. Closing connection.")
        await websocket.close()
        return

    async for data in websocket.iter_json():
        ride_service.process_message(data, websocket)
        print(f'Message received was: {data}')

    # WebSocketDisconnect raised
    ride_service.disconnect(websocket)
