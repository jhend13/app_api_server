from fastapi import WebSocket
from .user import User


class RideQueue():
    def __init__(self):
        self.queue: dict[str, User] = {}

    def join(self, user: User) -> bool:
        if user.uid not in self.queue:
            self.queue[user.uid] = user
            print(f'User {user.email} has joined the ride queue.')
            return True
        else:
            print('User is already in the queue.')
            return False

    def leave(self, user: User):
        if user.uid in self.queue:
            print(f'User {user.email} has left the ride queue.')
            del self.queue[user.uid]
