from fastapi import WebSocket


class RideQueue():
    def __init__(self):
        # a queue of riders who have "confirmed" their pickup/destination details.
        # some checks to include:
        # todo: only allow one UID in the queue at a time
        self.queue: dict[WebSocket, int | None] = {}

    def join(self, websocket):
        print('User has joined the ride queue.')
        for websocket in self.queue:
            pass

    def leave():
        pass
