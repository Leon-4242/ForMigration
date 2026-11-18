from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from infrastructure.services.messenger import MessengerService
from models.user import User
from system.admin.keyboard import build_notify_keyboard


class Notify(StatesGroup):
    notify = State()


async def command_notify(message: Message, user: User, messenger: MessengerService, state: FSMContext):
    await state.clear()
    await state.set_state(Notify.notify)

    await messenger.send_message(
        user=user,
        text="Введите текст рассылки, можете прикрепить изображение.",
        parse_mode=ParseMode.HTML,
    )


async def forming_notify(
    message: Message, user: User, messenger: MessengerService, state: FSMContext
):
    if message.photo:
        photo = message.photo[-1].file_id
        text = message.caption
    else:
        photo = None
        text = message.text

    text = text if text else ""
    if not text and not photo:
        return await messenger.send_message(user=user, text="Рассылка не может быть пустой.", parse_mode=ParseMode.HTML)

    await state.update_data(notify_text=text, notify_photo=photo)

    text = "Рассылка успешно создана. Отправить рассылку всем пользователям?\n\n--------------------------------\n\n" + text

    await messenger.send_message(
        user=user,
        text=text,
        photo=photo,
        parse_mode=ParseMode.HTML,
        reply_markup=build_notify_keyboard(),
    )


async def send_notify(callback: CallbackQuery, user: User, messenger: MessengerService, state: FSMContext):
    data = await state.get_data()
    notify_text = data["notify_text"]
    notify_photo = data["notify_photo"]

    await messenger.broadcast(
        from_user=user, text=notify_text, photo=notify_photo, parse_mode=ParseMode.HTML
    )
    await callback.message.delete()
    await state.clear()


async def cancel_notify(callback: CallbackQuery, user: User, messenger: MessengerService, state: FSMContext):
    await state.clear()
    await messenger.send_message(user=user, text="Рассылка отменена.")
