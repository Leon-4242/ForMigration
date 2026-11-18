from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from modules.infrastructure.commands import InfrastructureCommands
from modules.infrastructure.keyboard import (
    InfrastructureCallback,
    build_cancel,
    build_choose_building,
    build_choose_places,
    build_info_nav,
)
from modules.infrastructure.repository import InfrastructureRepository
from modules.infrastructure.types import BuildingType, InfrastructureInfoType


class AdminFlow(StatesGroup):
    building = State()
    places = State()
    info = State()


async def _send_command_text(
    message: Message,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
    command_id: InfrastructureCommands,
) -> None:
    await state.clear()
    text = infrastructure.get_text(command_id)
    if not text:
        await message.reply("Текст команды пока недоступен. Попробуй позже.")
        return
    await message.answer(text, parse_mode=ParseMode.HTML, reply_markup=build_cancel())


async def command_resettlement_dep(
    message: Message,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
) -> None:
    await _send_command_text(message, state, infrastructure, InfrastructureCommands.RESETTLEMENT_DEP)


async def command_recycle_dsl(
    message: Message,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
) -> None:
    await _send_command_text(message, state, infrastructure, InfrastructureCommands.RECYCLE_DSL)


async def command_gym_dsl(
    message: Message,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
) -> None:
    await _send_command_text(message, state, infrastructure, InfrastructureCommands.GYM_DSL)


async def command_admin_ds(
    message: Message,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
) -> None:
    await state.clear()
    if not infrastructure.get_buildings(InfrastructureInfoType.ADMIN):
        await message.reply("Данные по администрации пока недоступны. Попробуй позже.")
        return
    await message.reply(
        "Выбери Общежитие:⤵️",
        reply_markup=build_choose_building(infrastructure),
    )
    await state.set_state(AdminFlow.building)


async def choose_admin_building(
    callback: CallbackQuery,
    callback_data: InfrastructureCallback,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
) -> None:
    if callback_data.building is None:
        await callback.answer("Не выбрано общежитие")
        return

    places = infrastructure.get_places(callback_data.building, InfrastructureInfoType.ADMIN)
    if not places:
        await callback.answer("Нет данных для выбранного общежития", show_alert=True)
        return

    await state.update_data(building=callback_data.building)
    await state.set_state(AdminFlow.places)
    await callback.answer(f"✅ Выбрано {callback_data.building}")
    await callback.message.edit_text(
        "Выбери нужный вариант:⤵️",
        parse_mode=ParseMode.HTML,
        reply_markup=build_choose_places(infrastructure, callback_data.building),
    )


async def view_admin_information(
    callback: CallbackQuery,
    callback_data: InfrastructureCallback,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
) -> None:
    if callback_data.building is None or callback_data.place is None:
        await callback.answer("Не выбран вариант")
        return

    record = infrastructure.get(
        callback_data.building,
        InfrastructureInfoType.ADMIN,
        callback_data.place,
    )
    if record is None:
        await callback.answer("Информация не найдена", show_alert=True)
        return

    await state.update_data(building=callback_data.building)
    await state.set_state(AdminFlow.info)
    await callback.message.edit_text(
        record.text,
        parse_mode=ParseMode.HTML,
        reply_markup=build_info_nav(),
    )


async def back_to_building(
    callback: CallbackQuery,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
) -> None:
    await callback.answer("↩️ Возвращаюсь")
    await callback.message.edit_text(
        "Выбери Общежитие:⤵️",
        reply_markup=build_choose_building(infrastructure),
    )
    await state.set_state(AdminFlow.building)


async def back_to_places(
    callback: CallbackQuery,
    state: FSMContext,
    infrastructure: InfrastructureRepository,
) -> None:
    data = await state.get_data()
    building = BuildingType(data["building"])
    await callback.answer("↩️ Возвращаюсь")
    await callback.message.edit_text(
        "Выбери нужный вариант:⤵️",
        parse_mode=ParseMode.HTML,
        reply_markup=build_choose_places(infrastructure, building),
    )
    await state.set_state(AdminFlow.places)


async def cancel_flow(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("✅ Скрыто")
    await callback.message.delete()
