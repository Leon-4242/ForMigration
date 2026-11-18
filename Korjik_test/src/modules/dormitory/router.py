from aiogram import F
from aiogram.filters import Command, StateFilter

from modules.base.router import ModuleRouter
from modules.dormitory import handlers
from modules.dormitory.commands import DormitoryCommands
from modules.dormitory.handlers import Info
from modules.dormitory.keyboard import BuildingAction, BuildingCallback, InfoCallback
from modules.dormitory.middleware import DormitoryMiddleware
from modules.dormitory.navigation import NavigationAction, NavigationCallback
from modules.dormitory.repository import DormitoryRepository


class DormitoryRouter(ModuleRouter):
    def __init__(self, repository: DormitoryRepository) -> None:
        super().__init__()
        middleware = DormitoryMiddleware(repository)
        self.router.message.middleware(middleware)
        self.router.callback_query.middleware(middleware)
        self.register_handlers()

    def register_handlers(self) -> None:
        router = self.router

        router.message.register(
            handlers.command_information,
            Command(DormitoryCommands.INFORMATION),
        )

        router.callback_query.register(
            handlers.choose_building,
            BuildingCallback.filter(F.action == BuildingAction.BUILDING),
            StateFilter(Info.building),
        )
        router.callback_query.register(
            handlers.choose_corpus,
            BuildingCallback.filter(F.action == BuildingAction.CORPUS),
            StateFilter(Info.corpus),
        )
        router.callback_query.register(
            handlers.choose_floor,
            BuildingCallback.filter(F.action == BuildingAction.FLOOR),
            StateFilter(Info.floor),
        )
        router.callback_query.register(
            handlers.show_information,
            InfoCallback.filter(),
            StateFilter(Info.information),
        )

        router.callback_query.register(
            handlers.back_to_building,
            NavigationCallback.filter(F.action == NavigationAction.BACK),
            StateFilter(Info.corpus),
        )
        router.callback_query.register(
            handlers.back_to_corpus,
            NavigationCallback.filter(F.action == NavigationAction.BACK),
            StateFilter(Info.floor),
        )
        router.callback_query.register(
            handlers.back_to_floor,
            NavigationCallback.filter(F.action == NavigationAction.BACK),
            StateFilter(Info.information),
        )
        router.callback_query.register(
            handlers.back_to_information,
            NavigationCallback.filter(F.action == NavigationAction.BACK),
            StateFilter(Info.comenda, Info.roomcheck, Info.starosta),
        )

        router.callback_query.register(
            handlers.cancel_flow,
            NavigationCallback.filter(F.action == NavigationAction.CANCEL),
            StateFilter(
                Info.building,
                Info.corpus,
                Info.floor,
                Info.information,
                Info.comenda,
                Info.roomcheck,
                Info.starosta,
            ),
        )
