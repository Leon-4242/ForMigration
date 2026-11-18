from enum import StrEnum

from aiogram.types import BotCommand


class ConsumerCommands(StrEnum):
    WASH_CLOTHES = "wash_clothes"
    BEDCLOTHES = "bedclothes"
    FOOD = "food"
    SHOP = "shop"


ConsumerBotCommands = [
    BotCommand(command=ConsumerCommands.WASH_CLOTHES, description="Прачечная"),
    BotCommand(command=ConsumerCommands.BEDCLOTHES, description="График смены белья"),
    BotCommand(command=ConsumerCommands.FOOD, description="Столовая"),
    BotCommand(command=ConsumerCommands.SHOP, description="Магазин"),
]
