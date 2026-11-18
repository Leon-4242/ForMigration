from enum import StrEnum

from aiogram.types import BotCommand


class DormitoryCommands(StrEnum):
    INFORMATION = "information"


DormitoryBotCommands = [
    BotCommand(
        command=DormitoryCommands.INFORMATION,
        description="Информация по общежитию",
    ),
]
