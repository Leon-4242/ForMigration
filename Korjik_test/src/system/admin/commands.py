from enum import StrEnum

from aiogram.types import BotCommand


class AdminCommands(StrEnum):
    RESTART = "restart"
    ADMIN_HELP = "admin_help"
    SET_ADMIN = "set_admin"
    NOTIFY = "notify"


AdminBotCommands = [
    BotCommand(command=AdminCommands.RESTART.value, description="Перезапуск Коржика"),
    BotCommand(
        command=AdminCommands.ADMIN_HELP.value, description="Список команд администратора Коржика"
    ),
    BotCommand(command=AdminCommands.SET_ADMIN.value, description="Назначить администратора"),
    BotCommand(command=AdminCommands.NOTIFY.value, description="Сделать рассылку"),
]
