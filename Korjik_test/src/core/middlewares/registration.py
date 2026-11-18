from aiogram.fsm.middleware import BaseMiddleware
from aiogram.types import User as TelegramUser

from config.settings import AUTO_REGISTER_USERS
from infrastructure.services.users import UsersService
from models.user import User


class RegistrationMiddleware(BaseMiddleware):
    def __init__(self, users: UsersService):
        self.users = users

    async def __call__(self, handler, event, data):
        telegram_user: TelegramUser | None = data.get("event_from_user")
        if telegram_user is None:
            data["user"] = None
            return await handler(event, data)

        if AUTO_REGISTER_USERS:
            self.users.register(
                User(
                    telegram_id=telegram_user.id,
                    name=telegram_user.username or "",
                )
            )

        data["user"] = self.users.get_user(telegram_user.id)
        return await handler(event, data)
