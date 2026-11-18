from aiogram import Router

from system.echo.wrong_command import echo_error


class EchoRouter:
    def __init__(self):
        self.router = Router()

        self.router.message.register(echo_error)

    def get_router(self) -> Router:
        return self.router
