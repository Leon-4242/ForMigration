from enum import StrEnum

from models.sheet_types import SheetTypes


class Modules(StrEnum):
    DORMITORY = "dormitory"
    CONSUMER = "consumer"
    INFRASTRUCTURE = "infrastructure"
    HOROSCOPE = "horoscope"

def sheets_for_module(module: Modules) -> list[SheetTypes]:
    match module:
        case Modules.DORMITORY:
            return [SheetTypes.DORMITORY]
        case Modules.CONSUMER:
            return [SheetTypes.FOOD, SheetTypes.SHOP, SheetTypes.WASH]
        case Modules.INFRASTRUCTURE:
            return [SheetTypes.ADMIN, SheetTypes.INFO]
