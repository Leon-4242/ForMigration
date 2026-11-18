from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from modules.consumer.keyboard import (
    ConsumerCallback,
    build_choose_building,
    build_choose_places,
    build_info_nav,
)
from modules.consumer.repository import ConsumerRepository
from modules.consumer.types import ACTION_TO_INFO_TYPE, BuildingType, ConsumerAction

WASH_PLACE = "wash"
BEDCLOTHES_PLACE = "bedclothes"

_ACTION_PLACE: dict[ConsumerAction, str] = {
    ConsumerAction.WASH: WASH_PLACE,
    ConsumerAction.BEDCLOTHES: BEDCLOTHES_PLACE,
}


class ConsumerFlow(StatesGroup):
    building = State()
    places = State()
    info = State()


def _get_available_buildings(
    consumer: ConsumerRepository,
    action: ConsumerAction,
) -> list[BuildingType]:
    info_type = ACTION_TO_INFO_TYPE[action]
    if action in _ACTION_PLACE:
        place = _ACTION_PLACE[action]
        return [
            building
            for building in consumer.get_buildings(info_type)
            if consumer.get(building, info_type, place) is not None
        ]
    return consumer.get_buildings(info_type)


async def _start_flow(
    message: Message,
    state: FSMContext,
    consumer: ConsumerRepository,
    action: ConsumerAction,
    empty_text: str,
) -> None:
    await state.clear()
    buildings = _get_available_buildings(consumer, action)
    if not buildings:
        await message.reply(empty_text)
        return
    await message.reply(
        "Выбери Общежитие:⤵️",
        reply_markup=build_choose_building(consumer, action, buildings),
    )
    await state.set_state(ConsumerFlow.building)
    await state.update_data(action=action)


async def command_wash_clothes(
    message: Message,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    await _start_flow(
        message,
        state,
        consumer,
        ConsumerAction.WASH,
        "Данные по прачечной пока недоступны. Попробуй позже.",
    )


async def command_bedclothes(
    message: Message,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    await _start_flow(
        message,
        state,
        consumer,
        ConsumerAction.BEDCLOTHES,
        "Данные по смене белья пока недоступны. Попробуй позже.",
    )


async def command_food(
    message: Message,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    await _start_flow(
        message,
        state,
        consumer,
        ConsumerAction.FOOD,
        "Данные по столовым пока недоступны. Попробуй позже.",
    )


async def command_shop(
    message: Message,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    await _start_flow(
        message,
        state,
        consumer,
        ConsumerAction.SHOP,
        "Данные по магазинам пока недоступны. Попробуй позже.",
    )


async def choose_building(
    callback: CallbackQuery,
    callback_data: ConsumerCallback,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    info_type = ACTION_TO_INFO_TYPE[callback_data.action]
    await state.update_data(action=callback_data.action, building=callback_data.building)

    if callback_data.action in _ACTION_PLACE:
        place = _ACTION_PLACE[callback_data.action]
        record = consumer.get(callback_data.building, info_type, place)
        if record is None:
            await callback.answer("Информация не найдена", show_alert=True)
            return
        await state.set_state(ConsumerFlow.info)
        await callback.message.edit_text(
            record.text,
            parse_mode=ParseMode.HTML,
            reply_markup=build_info_nav(),
        )
        return

    places = consumer.get_places(callback_data.building, info_type)
    if not places:
        await callback.answer("Нет данных для выбранного общежития", show_alert=True)
        return

    await state.set_state(ConsumerFlow.places)
    await callback.message.edit_text(
        "Выбери нужный вариант:⤵️",
        parse_mode=ParseMode.HTML,
        reply_markup=build_choose_places(
            consumer,
            callback_data.building,
            callback_data.action,
        ),
    )


async def view_information(
    callback: CallbackQuery,
    callback_data: ConsumerCallback,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    if callback_data.place_idx is None:
        await callback.answer("Не выбран вариант")
        return

    info_type = ACTION_TO_INFO_TYPE[callback_data.action]
    places = consumer.get_places(callback_data.building, info_type)
    if callback_data.place_idx >= len(places):
        await callback.answer("Информация не найдена", show_alert=True)
        return

    record = consumer.get(callback_data.building, info_type, places[callback_data.place_idx])
    if record is None:
        await callback.answer("Информация не найдена", show_alert=True)
        return

    await state.update_data(action=callback_data.action, building=callback_data.building)
    await state.set_state(ConsumerFlow.info)
    await callback.message.edit_text(
        record.text,
        parse_mode=ParseMode.HTML,
        reply_markup=build_info_nav(),
    )


async def back_to_building(
    callback: CallbackQuery,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    data = await state.get_data()
    action = ConsumerAction(data["action"])
    buildings = _get_available_buildings(consumer, action)
    await callback.answer("↩️ Возвращаюсь")
    await callback.message.edit_text(
        "Выбери Общежитие:⤵️",
        reply_markup=build_choose_building(consumer, action, buildings),
    )
    await state.set_state(ConsumerFlow.building)


async def back_to_places(
    callback: CallbackQuery,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    data = await state.get_data()
    action = ConsumerAction(data["action"])
    building = BuildingType(data["building"])
    await callback.answer("↩️ Возвращаюсь")
    await callback.message.edit_text(
        "Выбери нужный вариант:⤵️",
        parse_mode=ParseMode.HTML,
        reply_markup=build_choose_places(consumer, building, action),
    )
    await state.set_state(ConsumerFlow.places)


async def back_from_info(
    callback: CallbackQuery,
    state: FSMContext,
    consumer: ConsumerRepository,
) -> None:
    data = await state.get_data()
    action = ConsumerAction(data["action"])
    if action in _ACTION_PLACE:
        await back_to_building(callback, state, consumer)
    else:
        await back_to_places(callback, state, consumer)


async def cancel_flow(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("✅ Скрыто")
    await callback.message.delete()
