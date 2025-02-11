import asyncio
from fastapi import WebSocket
from enum import Enum
from app.services.ride import RideQueue
from .user import User


class ActionTypes(Enum):
    AUTHENTICATE = 'authenticate'
    SERVICE_STATE = 'serviceState'
    ROUTE_CONFIRM = 'routeConfirm'
    RIDE_CANCEL = 'rideCancel'
    RIDE_START = 'rideStart'
    RIDE_END = 'rideEnd'


class RideService():
    def __init__(self):
        self.available_drivers = 0
        self.connections: dict[WebSocket, int | None] = {}
        self.ride_pool = RideQueue()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        print('Client connected')
        self.connections[websocket] = None
        await self.send_message(websocket, ActionTypes.AUTHENTICATE)

    def disconnect(self, websocket):
        print(f'{self.connections[websocket]} disconnected.')
        del self.connections[websocket]

    def process_message(self, data, websocket):
        action = ActionTypes(data['action'])

        print(f'Message received: {action}')

        match action:
            case ActionTypes.SERVICE_STATE:
                # todo replace this with
                # was this just a place holder lol? ...
                asyncio.create_task(self.send_message(
                    websocket, ActionTypes.AUTHENTICATE))
            case ActionTypes.ROUTE_CONFIRM:
                self.on_route_confirm(websocket)
            case ActionTypes.RIDE_CANCEL:
                self.on_ride_cancel(websocket)

    async def send_message(self, websocket, action_type: ActionTypes, data=None):
        payload = {
            'action': action_type.value,
            'data': data
        }
        print(f'Sending payload: {payload}')
        await websocket.send_json(payload)

    def on_route_confirm(self, websocket: WebSocket):
        if hasattr(websocket, '_aadd_user'):
            if self.ride_pool.join(websocket._aadd_user):
                asyncio.create_task(self.send_message(
                    websocket, ActionTypes.ROUTE_CONFIRM))
        else:
            print('invalid action')

    def on_ride_cancel(self, websocket: WebSocket):
        if hasattr(websocket, '_aadd_user'):
            self.ride_pool.leave(websocket._aadd_user)

    def is_authenticated(self, websocket: WebSocket):
        return hasattr(websocket, '_aadd_user')

    # associates a User with a websocket
    def user_authenticated(self, websocket: WebSocket, user: User):
        print('User authenticated.')
        websocket._aadd_user = user
