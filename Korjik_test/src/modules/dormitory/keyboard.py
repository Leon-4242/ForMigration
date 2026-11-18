from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.dormitory.navigation import add_back, add_cancel
from modules.dormitory.repository import DormitoryRepository
from modules.dormitory.types import BuildingType, CorpusType, InfoType


class BuildingAction(StrEnum):
    BUILDING = "building"
    CORPUS = "corpus"
    FLOOR = "floor"


class BuildingCallback(CallbackData, prefix="build"):
    action: BuildingAction
    building: BuildingType | None = None
    corpus: CorpusType | None = None
    floor: int | None = None


class InfoCallback(CallbackData, prefix="info"):
    action: InfoType


def _adjust_with_nav(builder: InlineKeyboardBuilder, item_count: int, items_per_row: int) -> None:
    rows: list[int] = []
    remaining = item_count
    while remaining > 0:
        row = min(items_per_row, remaining)
        rows.append(row)
        remaining -= row
    rows.append(2)
    builder.adjust(*rows)


def build_choose_building(repository: DormitoryRepository):
    builder = InlineKeyboardBuilder()
    buildings = repository.get_buildings()

    for building in buildings:
        builder.button(
            text=str(building),
            callback_data=BuildingCallback(
                building=building,
                action=BuildingAction.BUILDING,
            ),
        )

    add_cancel(builder)
    builder.adjust(max(len(buildings), 1), 1)

    return builder.as_markup()


def build_choose_corpus(repository: DormitoryRepository, building: BuildingType):
    builder = InlineKeyboardBuilder()
    corpuses = repository.get_corpuses(building)

    for corpus in corpuses:
        builder.button(
            text=str(corpus),
            callback_data=BuildingCallback(
                building=building,
                corpus=corpus,
                action=BuildingAction.CORPUS,
            ),
        )

    add_back(builder)
    add_cancel(builder)
    builder.adjust(max(len(corpuses), 1), 2)

    return builder.as_markup()


def build_choose_floor(
    repository: DormitoryRepository,
    building: BuildingType,
    corpus: CorpusType,
):
    builder = InlineKeyboardBuilder()
    floors = repository.get_floors(building, corpus)

    for floor in floors:
        builder.button(
            text=str(floor),
            callback_data=BuildingCallback(
                building=building,
                corpus=corpus,
                floor=floor,
                action=BuildingAction.FLOOR,
            ),
        )

    add_back(builder)
    add_cancel(builder)
    _adjust_with_nav(builder, len(floors), items_per_row=8)

    return builder.as_markup()


def build_choose_information():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="Моя коменда",
        callback_data=InfoCallback(action=InfoType.COMENDA),
    )
    builder.button(
        text="Расписание проверок",
        callback_data=InfoCallback(action=InfoType.ROOMCHECK),
    )
    builder.button(
        text="Старосты моего этажа",
        callback_data=InfoCallback(action=InfoType.STAROSTA),
    )

    add_back(builder)
    add_cancel(builder)
    builder.adjust(1, 1, 1, 2)

    return builder.as_markup()


def build_info():
    builder = InlineKeyboardBuilder()

    add_back(builder)
    add_cancel(builder)

    return builder.as_markup()
