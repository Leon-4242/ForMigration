from abc import ABC, abstractmethod

from aiogram import Router


class ModuleRouter(ABC):
    """Базовый класс для aiogram-роутера модуля."""

    def __init__(self) -> None:
        self.router = Router()

    @abstractmethod
    def register_handlers(self) -> None:
        raise NotImplementedError

    def get_router(self) -> Router:
        return self.router
