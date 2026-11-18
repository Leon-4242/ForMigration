from aiogram.types import BotCommandScopeChat, BotCommand

from core.bot import TelegramBot
from infrastructure.services.users import UsersService
from models.user import User


class BotCommandsService:
    def __init__(self, user_commands: list[BotCommand], admin_commands: list[BotCommand], bot: TelegramBot):
        self.bot = bot
        self.user_commands = user_commands
        self.admin_commands = admin_commands

    async def setup_default(self) -> None:
        await self.bot.setup_commands(self.user_commands)

    async def sync_user(self, user: User) -> None:
        commands = self.admin_commands if user.admin else self.user_commands
        scope = BotCommandScopeChat(chat_id=user.telegram_id)
        await self.bot.setup_commands(commands, scope=scope)

    async def sync_admins(self, users: UsersService) -> None:
        for admin in users.get_admins():
            await self.sync_user(admin)

    async def setup_all(self, users: UsersService) -> None:
        await self.setup_default()
        await self.sync_admins(users)

    def close(self) -> None:
        pass
