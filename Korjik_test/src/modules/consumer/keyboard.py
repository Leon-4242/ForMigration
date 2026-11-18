from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.consumer.repository import ConsumerRepository
from modules.consumer.types import (
    ACTION_TO_INFO_TYPE,
    BuildingType,
    ConsumerAction,
    ConsumerStatus,
)


class NavigationAction(StrEnum):
    BACK = "back"
    CANCEL = "cancel"


class NavigationCallback(CallbackData, prefix="cons-nav"):
    action: NavigationAction


def add_back(builder: InlineKeyboardBuilder) -> None:
    builder.button(
        text="↩️ Назад",
        callback_data=NavigationCallback(action=NavigationAction.BACK),
    )


def add_cancel(builder: InlineKeyboardBuilder) -> None:
    builder.button(
        text="❌ Отмена",
        callback_data=NavigationCallback(action=NavigationAction.CANCEL),
    )


class ConsumerCallback(CallbackData, prefix="consumer"):
    building: BuildingType
    status: ConsumerStatus
    action: ConsumerAction
    place_idx: int | None = None


def build_cancel():
    builder = InlineKeyboardBuilder()
    add_cancel(builder)
    return builder.as_markup()


def build_info_nav():
    builder = InlineKeyboardBuilder()
    add_back(builder)
    add_cancel(builder)
    builder.adjust(2)
    return builder.as_markup()


def _adjust_with_nav(builder: InlineKeyboardBuilder, item_count: int, items_per_row: int) -> None:
    rows: list[int] = []
    remaining = item_count
    while remaining > 0:
        row = min(items_per_row, remaining)
        rows.append(row)
        remaining -= row
    rows.append(2)
    builder.adjust(*rows)


def build_choose_building(
    repository: ConsumerRepository,
    action: ConsumerAction,
    buildings: list[BuildingType] | None = None,
):
    builder = InlineKeyboardBuilder()
    if buildings is None:
        info_type = ACTION_TO_INFO_TYPE[action]
        buildings = repository.get_buildings(info_type)

    for building in buildings:
        builder.button(
            text=str(building),
            callback_data=ConsumerCallback(
                building=building,
                status=ConsumerStatus.CHOICE,
                action=action,
            ),
        )

    add_cancel(builder)
    builder.adjust(max(len(buildings), 1), 1)

    return builder.as_markup()


def build_choose_places(
    repository: ConsumerRepository,
    building: BuildingType,
    action: ConsumerAction,
):
    builder = InlineKeyboardBuilder()
    info_type = ACTION_TO_INFO_TYPE[action]
    places = repository.get_places(building, info_type)

    for place_idx, place in enumerate(places):
        builder.button(
            text=place,
            callback_data=ConsumerCallback(
                building=building,
                status=ConsumerStatus.READ,
                action=action,
                place_idx=place_idx,
            ),
        )

    add_back(builder)
    add_cancel(builder)
    _adjust_with_nav(builder, len(places), items_per_row=2)

    return builder.as_markup()
