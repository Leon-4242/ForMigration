from aiogram.enums import ParseMode
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.lifecycle import BotLifecycle
from infrastructure.services.bot_commands import BotCommandsService
from infrastructure.services.messages import MessageService
from infrastructure.services.messenger import MessengerService
from infrastructure.services.users import UsersService
from models.message import MessageTypes
from models.user import User
from system.admin.commands import AdminCommands


async def command_restart(
    message: Message,
    user: User,
    messenger: MessengerService,
    lifecycle: BotLifecycle,
    state: FSMContext,
):
    await state.clear()
    await messenger.broadcast_admin(text="Перезапуск Коржика")
    await lifecycle.restart()


async def command_admin_help(
    message: Message,
    user: User, messages: MessageService, messenger: MessengerService, state: FSMContext
):
    await state.clear()
    admin_help_message = messages.get_text(MessageTypes.COMMAND, AdminCommands.ADMIN_HELP)
    await messenger.send_message(user=user, text=admin_help_message, parse_mode=ParseMode.HTML)


async def command_set_admin(
    message: Message,
    user: User,
    users: UsersService,
    messenger: MessengerService,
    bot_commands: BotCommandsService,
    command: CommandObject,
    state: FSMContext,
):
    await state.clear()

    if command.args is None:
        await messenger.send_message(
            user=user,
            text="Используйте /set_admin <username> <1 или 0>\nПример: /set_admin vls4m 1",
        )
        return

    parts = command.args.split()
    if len(parts) < 2:
        await messenger.send_message(
            user=user,
            text="Используйте /set_admin <username> <1 или 0>\nПример: /set_admin vls4m 1",
        )
        return

    username, admin_flag_raw = parts[0], parts[1]
    try:
        admin_flag = bool(int(admin_flag_raw))
    except ValueError:
        await messenger.send_message(user=user, text="Флаг admin должен быть 0 или 1")
        return

    target_user = users.get_user_by_name(name=username)
    if target_user is None:
        await messenger.send_message(user=user, text=f"Пользователь {username} не найден")
        return

    users.set_admin(target_user, admin_flag)
    updated_user = users.get_user(target_user.telegram_id)
    if updated_user is None:
        await messenger.send_message(user=user, text="Не удалось обновить пользователя")
        return

    await bot_commands.sync_user(updated_user)

    status = "назначен" if admin_flag else "снят"
    await messenger.broadcast_admin(
        from_user=user,
        text=f"Пользователь @{username} {status} администратором",
    )
