from aiogram import F
from aiogram.filters import Command, StateFilter

from modules.base.router import ModuleRouter
from modules.consumer import handlers
from modules.consumer.commands import ConsumerCommands
from modules.consumer.handlers import ConsumerFlow
from modules.consumer.keyboard import (
    ConsumerCallback,
    ConsumerStatus,
    NavigationAction,
    NavigationCallback,
)
from modules.consumer.middleware import ConsumerMiddleware
from modules.consumer.repository import ConsumerRepository


class ConsumerRouter(ModuleRouter):
    def __init__(self, repository: ConsumerRepository) -> None:
        super().__init__()
        middleware = ConsumerMiddleware(repository)
        self.router.message.middleware(middleware)
        self.router.callback_query.middleware(middleware)
        self.register_handlers()

    def register_handlers(self) -> None:
        router = self.router

        router.message.register(
            handlers.command_wash_clothes,
            Command(ConsumerCommands.WASH_CLOTHES),
        )
        router.message.register(
            handlers.command_bedclothes,
            Command(ConsumerCommands.BEDCLOTHES),
        )
        router.message.register(
            handlers.command_food,
            Command(ConsumerCommands.FOOD),
        )
        router.message.register(
            handlers.command_shop,
            Command(ConsumerCommands.SHOP),
        )

        router.callback_query.register(
            handlers.choose_building,
            ConsumerCallback.filter(F.status == ConsumerStatus.CHOICE),
            StateFilter(ConsumerFlow.building),
        )
        router.callback_query.register(
            handlers.view_information,
            ConsumerCallback.filter(F.status == ConsumerStatus.READ),
            StateFilter(ConsumerFlow.places),
        )

        router.callback_query.register(
            handlers.back_to_building,
            NavigationCallback.filter(F.action == NavigationAction.BACK),
            StateFilter(ConsumerFlow.places),
        )
        router.callback_query.register(
            handlers.back_from_info,
            NavigationCallback.filter(F.action == NavigationAction.BACK),
            StateFilter(ConsumerFlow.info),
        )

        router.callback_query.register(
            handlers.cancel_flow,
            NavigationCallback.filter(F.action == NavigationAction.CANCEL),
        )
