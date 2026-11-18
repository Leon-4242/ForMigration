from collections.abc import Callable

from modules.base import BotModule
from modules.consumer.module import ConsumerModule
from modules.context import ModuleContext
from modules.dormitory.module import DormitoryModule
from modules.horoscope.module import HoroscopeModule
from modules.infrastructure.module import InfrastructureModule

ModuleFactory = Callable[[ModuleContext], BotModule]

# Добавление модуля:
#   1) реализовать BotModule по образцу modules/base/
#   2) добавить фабрику в MODULE_FACTORIES
MODULE_FACTORIES: list[ModuleFactory] = [
    lambda ctx: DormitoryModule(ctx),
    lambda ctx: ConsumerModule(ctx),
    lambda ctx: InfrastructureModule(ctx),
    lambda ctx: HoroscopeModule(ctx),
]


def build_modules(context: ModuleContext) -> list[BotModule]:
    return [factory(context) for factory in MODULE_FACTORIES]
