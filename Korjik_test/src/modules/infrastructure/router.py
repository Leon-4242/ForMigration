from aiogram import F
from aiogram.filters import Command, StateFilter

from modules.base.router import ModuleRouter
from modules.infrastructure import handlers
from modules.infrastructure.commands import InfrastructureCommands
from modules.infrastructure.handlers import AdminFlow
from modules.infrastructure.keyboard import (
    InfrastructureCallback,
    InfrastructureStatus,
    NavigationAction,
    NavigationCallback,
)
from modules.infrastructure.middleware import InfrastructureMiddleware
from modules.infrastructure.repository import InfrastructureRepository


class InfrastructureRouter(ModuleRouter):
    def __init__(self, repository: InfrastructureRepository) -> None:
        super().__init__()
        middleware = InfrastructureMiddleware(repository)
        self.router.message.middleware(middleware)
        self.router.callback_query.middleware(middleware)
        self.register_handlers()

    def register_handlers(self) -> None:
        router = self.router

        router.message.register(
            handlers.command_resettlement_dep,
            Command(InfrastructureCommands.RESETTLEMENT_DEP),
        )
        router.message.register(
            handlers.command_recycle_dsl,
            Command(InfrastructureCommands.RECYCLE_DSL),
        )
        router.message.register(
            handlers.command_gym_dsl,
            Command(InfrastructureCommands.GYM_DSL),
        )
        router.message.register(
            handlers.command_admin_ds,
            Command(InfrastructureCommands.ADMIN_DS),
        )

        router.callback_query.register(
            handlers.choose_admin_building,
            InfrastructureCallback.filter(F.status == InfrastructureStatus.CHOICE),
            StateFilter(AdminFlow.building),
        )
        router.callback_query.register(
            handlers.view_admin_information,
            InfrastructureCallback.filter(F.status == InfrastructureStatus.READ),
            StateFilter(AdminFlow.places),
        )

        router.callback_query.register(
            handlers.back_to_building,
            NavigationCallback.filter(F.action == NavigationAction.BACK),
            StateFilter(AdminFlow.places),
        )
        router.callback_query.register(
            handlers.back_to_places,
            NavigationCallback.filter(F.action == NavigationAction.BACK),
            StateFilter(AdminFlow.info),
        )

        router.callback_query.register(
            handlers.cancel_flow,
            NavigationCallback.filter(F.action == NavigationAction.CANCEL),
        )
