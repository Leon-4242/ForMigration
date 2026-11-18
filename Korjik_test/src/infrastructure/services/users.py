from database.users import UsersDatabase
from models.user import User


class UsersService:
    def __init__(self, users: UsersDatabase):
        self.users = users

    def add_user(self, user: User) -> None:
        self.users.add_user(user=user)

    def get_user(self, telegram_id: int) -> User | None:
        return self.users.get_by_id(telegram_id=telegram_id)

    def get_user_by_name(self, name: str) -> User | None:
        return self.users.get_by_name(name=name)

    def exist_user(self, user: User) -> bool:
        return self.get_user(user.telegram_id) is not None

    def register(self, user: User) -> None:
        if not self.exist_user(user):
            self.add_user(user)

    def set_admin(self, user: User, admin: bool) -> str:
        if self.exist_user(user):
            self.users.set_admin(telegram_id=user.telegram_id, admin=admin)
            return "set_admin: success"
        return "set_admin: failed, I don't know this user"

    def get_users(self) -> list[User]:
        return self.users.get_users()

    def get_admins(self) -> list[User]:
        return self.users.get_admins()

    def close(self):
        pass
