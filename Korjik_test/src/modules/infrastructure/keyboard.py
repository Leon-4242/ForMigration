from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.infrastructure.repository import InfrastructureRepository
from modules.infrastructure.types import (
    BuildingType,
    InfrastructureAction,
    InfrastructureInfoType,
    InfrastructureStatus,
)


class NavigationAction(StrEnum):
    BACK = "back"
    CANCEL = "cancel"


class NavigationCallback(CallbackData, prefix="infra-nav"):
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


class InfrastructureCallback(CallbackData, prefix="infra"):
    status: InfrastructureStatus
    action: InfrastructureAction
    building: BuildingType | None = None
    place: str | None = None


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


def build_choose_building(repository: InfrastructureRepository):
    builder = InlineKeyboardBuilder()
    buildings = repository.get_buildings(InfrastructureInfoType.ADMIN)

    for building in buildings:
        builder.button(
            text=str(building),
            callback_data=InfrastructureCallback(
                status=InfrastructureStatus.CHOICE,
                action=InfrastructureAction.ADMIN,
                building=building,
            ),
        )

    add_cancel(builder)
    builder.adjust(max(len(buildings), 1), 1)

    return builder.as_markup()


def build_choose_places(
    repository: InfrastructureRepository,
    building: BuildingType,
):
    builder = InlineKeyboardBuilder()
    places = repository.get_places(building, InfrastructureInfoType.ADMIN)

    for place in places:
        builder.button(
            text=place,
            callback_data=InfrastructureCallback(
                status=InfrastructureStatus.READ,
                action=InfrastructureAction.ADMIN,
                building=building,
                place=place,
            ),
        )

    add_back(builder)
    add_cancel(builder)

    rows: list[int] = []
    remaining = len(places)
    while remaining > 0:
        row = min(2, remaining)
        rows.append(row)
        remaining -= row
    rows.append(2)
    builder.adjust(*rows)

    return builder.as_markup()
