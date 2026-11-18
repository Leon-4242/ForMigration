from enum import StrEnum

from aiogram.types import BotCommand


class HoroscopeCommands(StrEnum):
    HELP = "horo_help"
    SUB = "horo_sub"
    UNSUB = "horo_unsub"
    TIME = "horo_time"


HoroscopeBotCommands = [
    BotCommand(command=HoroscopeCommands.HELP, description="Помощь по гороскопу"),
    BotCommand(command=HoroscopeCommands.SUB, description="Подписаться на гороскоп"),
    BotCommand(command=HoroscopeCommands.UNSUB, description="Отписаться от гороскопа"),
    BotCommand(command=HoroscopeCommands.TIME, description="Время утреннего гороскопа"),
]

HELP_TEXT = (
    "<b>Гороскоп</b>\n\n"
    "/horo_sub — подписаться на ежедневные открытки и гороскоп (по умолчанию в 7:00)\n"
    "/horo_unsub — отписаться\n"
    "/horo_time ЧЧ ММ — изменить время, например: /horo_time 13 44"
)
