import logging

from core.bot import TelegramBot
from infrastructure.services.users import UsersService
from models.user import User


class MessengerService:
    def __init__(self, bot: TelegramBot, users: UsersService):
        self.bot = bot
        self.users = users

    async def send_message(self, user: User, text: str, photo: str | None = None, **kwargs):
        if photo is not None:
            return await self.bot.send_photo(
                chat_id=user.telegram_id, photo=photo, caption=text, **kwargs
            )
        else:
            return await self.bot.send_message(chat_id=user.telegram_id, text=text, **kwargs)

    async def notify_users(
        self,
        users: list[User],
        text: str,
        photo: str | None = None,
        from_user: User | None = None,
        **kwargs,
    ):
        success: int = 0

        failed: list[dict] = []
        for user in users:
            try:
                await self.send_message(user=user, text=text, photo=photo, **kwargs)
            except Exception as e:
                failed.append({"user": user, "except": e})

        success = len(users) - len(failed)

        logging.info("Notifying failed for: [{}]".format(", ".join(map(str, failed))))

        return {"success": success, "failed": failed}

    async def broadcast(
        self, text: str, photo: str | None = None, from_user: User | None = None, **kwargs
    ):
        users = self.users.get_users()
        return await self.notify_users(
            users=users, text=text, photo=photo, from_user=from_user, **kwargs
        )

    async def broadcast_admin(
        self, text: str, photo: str | None = None, from_user: User | None = None, **kwargs
    ):
        users = self.users.get_admins()
        return await self.notify_users(
            users=users, text=text, photo=photo, from_user=from_user, **kwargs
        )

    def close(self):
        pass
