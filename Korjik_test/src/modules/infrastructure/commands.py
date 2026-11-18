from enum import StrEnum

from aiogram.types import BotCommand


class InfrastructureCommands(StrEnum):
    RESETTLEMENT_DEP = "resettlement_dep"
    RECYCLE_DSL = "recycle_dsl"
    GYM_DSL = "gym_dsl"
    ADMIN_DS = "admin_ds"


InfrastructureBotCommands = [
    BotCommand(command=InfrastructureCommands.RESETTLEMENT_DEP, description="Отдел ресселения в ДС"),
    BotCommand(command=InfrastructureCommands.RECYCLE_DSL, description="Переработка отходов в ДСЛ"),
    BotCommand(command=InfrastructureCommands.GYM_DSL, description="Тренажерный зал в ДСЛ"),
    BotCommand(command=InfrastructureCommands.ADMIN_DS, description="Администрация"),
]
