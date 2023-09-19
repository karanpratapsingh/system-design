from exceptions import AlreadyExists, DoesNotExists
from models.user import User


class UserRepo:
    def __init__(self) -> None:
        self.users = {}

    def register_user(self, user: User) -> User:
        if self.users.get(user.email):
            raise AlreadyExists("user with given mail already exists")
        user.id = user.email
        self.users[user.id] = user
        return user

    def get(self, user_id: str) -> User:
        if not self.users.get(user_id):
            raise DoesNotExists("user with given id does not exists")
        return self.users[user_id]
