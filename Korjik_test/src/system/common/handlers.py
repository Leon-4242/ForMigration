from aiogram.enums import ParseMode
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.services.messages import MessageService
from infrastructure.services.messenger import MessengerService
from infrastructure.services.users import UsersService
from models.message import MessageTypes
from models.user import User
from system.common.commands import CommonCommands


async def command_start(
    message: Message,
    user: User | None,
    messages: MessageService,
    users: UsersService,
    messenger: MessengerService,
    state: FSMContext,
):
    await state.clear()
    if user is None:
        from_user = User(
            telegram_id=message.from_user.id,
            name=message.from_user.username if message.from_user.username else "",
        )
        users.add_user(from_user)
    else:
        from_user = user
    start_message = messages.get_text(MessageTypes.COMMAND, CommonCommands.START)

    await messenger.send_message(user=from_user, text=start_message, parse_mode=ParseMode.HTML)


async def command_help(
    message: Message,
    user: User | None,
    messages: MessageService,
    messenger: MessengerService,
    state: FSMContext,
):
    await state.clear()
    help_message = messages.get_text(MessageTypes.COMMAND, CommonCommands.HELP)

    await messenger.send_message(user=user, text=help_message, parse_mode=ParseMode.HTML)


async def command_feedback(
    message: Message,
    user: User,
    messenger: MessengerService,
    command: CommandObject,
    state: FSMContext,
):
    await state.clear()

    text = command.args
    if text:
        await messenger.broadcast_admin(
            text=f"Обратная связь от \n@{user.name}\n{message.from_user.full_name}:\n{text}"
        )
        await messenger.send_message(user=user, text="Фидбек отправлен!")
    else:
        await messenger.send_message(user=user, text="/feedback [ваше обращение]")
