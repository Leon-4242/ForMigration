from enum import StrEnum

from aiogram.types import BotCommand


class CommonCommands(StrEnum):
    START = "start"
    HELP = "help"
    FEEDBACK = "feedback"


CommonBotCommands = [
    BotCommand(command=CommonCommands.START.value, description="Запуск Коржика"),
    BotCommand(command=CommonCommands.HELP.value, description="Список команд Коржика"),
    BotCommand(command=CommonCommands.FEEDBACK.value, description="Отправить отзыв/предложение"),
]
