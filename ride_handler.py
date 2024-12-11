
from fastapi import WebSocket
from enum import Enum


class ActionTypes(Enum):
    REGISTER_CLIENT = 'registerClient'
    SERVICE_STATE = 'serviceState'
    ROUTE_CONFIRM = 'routeConfirm'
    RIDE_START = 'rideStart'
    RIDE_END = 'rideEnd'


class RideService():
    driver_pool = 23

    # to determine: how should this be indexed? by user id?
    # should it be a list? or a dict for unqiue 1-1?
    websockets = {}

    def on_connect(self, user_id):
        pass

    def on_disconnect(self, user_id):
        pass

    def process_message(self, user_id, data):
        action = ActionTypes(data['action'])

        match action:
            case ActionTypes.SERVICE_STATE:
                self.send_message()

    def send_message(self, user_id, action_type: ActionTypes, data=None):
        payload = {
            'action': action_type.value,
            'data': data
        }
        self.websockets[user_id].send_json(payload)
