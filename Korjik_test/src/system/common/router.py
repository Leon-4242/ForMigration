from aiogram import Router
from aiogram.filters import Command

from system.common.commands import CommonCommands
from system.common.handlers import command_feedback, command_help, command_start


class UserRouter:
    def __init__(self):
        self.router = Router()

        self.router.message.register(command_start, Command(CommonCommands.START))
        self.router.message.register(command_help, Command(CommonCommands.HELP))
        self.router.message.register(command_feedback, Command(CommonCommands.FEEDBACK))

    def get_router(self) -> Router:
        return self.router
