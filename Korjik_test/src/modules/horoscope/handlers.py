from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from modules.horoscope.commands import HELP_TEXT
from modules.horoscope.service import HoroscopeService


async def command_help(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(HELP_TEXT, parse_mode=ParseMode.HTML)


async def command_subscribe(message: Message, horoscope: HoroscopeService) -> None:
    user_id = message.from_user.id
    username = message.from_user.username

    if not await horoscope.add_subscription(user_id, username):
        await message.answer("Вы уже получаете ежедневные сообщения (:")
        return

    await message.answer(
        "Теперь каждое утро в 7:00 я буду присылать свои отобранные открытки и гороскоп 🥰🥳"
    )


async def command_unsubscribe(message: Message, horoscope: HoroscopeService) -> None:
    user_id = message.from_user.id

    if not await horoscope.remove_subscription(user_id):
        await message.answer("Ты ещё не подписан на гороскоп.")
        return

    await message.answer("Теперь я не буду присылать каждое утро тебе открытку и гороскоп:(")


async def command_set_time(message: Message, horoscope: HoroscopeService) -> None:
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Попробуй пожалуйста /horo_time hour minutes")
        return

    hour_text, minute_text = parts[1], parts[2]
    if not (hour_text.isdigit() and minute_text.isdigit()):
        await message.answer(
            "Попробуй пожалуйста /horo_time hour minutes цифрами.\n"
            "Example: /horo_time 13 44"
        )
        return

    hour, minute = int(hour_text), int(minute_text)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        await message.answer(
            "Попробуй пожалуйста /horo_time hour minutes цифрами.\n"
            "Example: /horo_time 13 44"
        )
        return

    if not await horoscope.set_notify_time(message.from_user.id, hour, minute):
        await message.answer("Сначала подпишись на гороскоп: /horo_sub")
        return

    await message.answer(
        f"Теперь я буду желать тебе самого доброго утра в {hour:02d}:{minute:02d} 🥰🥳"
    )
