from fastapi import WebSocket
from enum import Enum
from .ride_queue import RideQueue

# must match client action type


class ActionTypes(Enum):
    AUTHENTICATE = 'authenticate'
    SERVICE_STATE = 'serviceState'
    ROUTE_CONFIRM = 'routeConfirm'
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
                self.send_message(websocket, ActionTypes.AUTHENTICATE)

    async def send_message(self, websocket, action_type: ActionTypes, data=None):
        payload = {
            'action': action_type.value,
            'data': data
        }
        print(f'Sending payload: {payload}')
        await websocket.send_json(payload)
        # self.websockets[user_id].send_json(payload)
