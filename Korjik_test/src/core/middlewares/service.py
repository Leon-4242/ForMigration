from aiogram.fsm.middleware import BaseMiddleware

from core.lifecycle import BotLifecycle
from infrastructure.services.bot_commands import BotCommandsService
from infrastructure.services.messages import MessageService
from infrastructure.services.messenger import MessengerService
from infrastructure.services.users import UsersService


class ServiceMiddleware(BaseMiddleware):
    def __init__(
        self,
        messenger: MessengerService,
        messages: MessageService,
        users: UsersService,
        lifecycle: BotLifecycle,
        bot_commands: BotCommandsService,
    ):
        self.messenger = messenger
        self.messages = messages
        self.users = users
        self.lifecycle = lifecycle
        self.bot_commands = bot_commands

    async def __call__(self, handler, event, data):
        data["messenger"] = self.messenger
        data["messages"] = self.messages
        data["users"] = self.users
        data["lifecycle"] = self.lifecycle
        data["bot_commands"] = self.bot_commands
        return await handler(event, data)
