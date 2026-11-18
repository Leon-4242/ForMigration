from aiogram.types import Message


async def echo_error(message: Message):
    await message.answer("Я не распознал твоей команды. Напиши /help.")
