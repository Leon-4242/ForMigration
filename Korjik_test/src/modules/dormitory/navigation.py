from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class NavigationAction(StrEnum):
    BACK = "back"
    CANCEL = "cancel"


class NavigationCallback(CallbackData, prefix="nav"):
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
