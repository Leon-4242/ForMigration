from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class NotifyCallback(CallbackData, prefix="notify"):
    send: bool


def build_notify_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text="Отправить", callback_data=NotifyCallback(send=True))
    builder.button(text="Отменить", callback_data=NotifyCallback(send=False))

    builder.adjust(2)
    return builder.as_markup()
