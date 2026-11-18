from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from modules.dormitory.keyboard import (
    BuildingCallback,
    InfoCallback,
    build_choose_building,
    build_choose_corpus,
    build_choose_floor,
    build_choose_information,
    build_info,
)
from modules.dormitory.repository import DormitoryRepository
from modules.dormitory.types import BuildingType, CorpusType, InfoType


class Info(StatesGroup):
    building = State()
    corpus = State()
    floor = State()
    information = State()
    comenda = State()
    roomcheck = State()
    starosta = State()


_INFO_STATES = {
    InfoType.COMENDA: Info.comenda,
    InfoType.ROOMCHECK: Info.roomcheck,
    InfoType.STAROSTA: Info.starosta,
}


async def command_information(
    message: Message,
    state: FSMContext,
    dormitory: DormitoryRepository,
) -> None:
    await state.clear()
    if not dormitory.get_buildings():
        await message.reply("Данные по общежитию пока недоступны. Попробуй позже.")
        return

    await message.reply(
        "Выбери Общежитие:⤵️",
        reply_markup=build_choose_building(dormitory),
    )
    await state.set_state(Info.building)


async def choose_building(
    callback: CallbackQuery,
    callback_data: BuildingCallback,
    state: FSMContext,
    dormitory: DormitoryRepository,
) -> None:
    if callback_data.building is None:
        await callback.answer("Не выбрано общежитие")
        return

    corpuses = dormitory.get_corpuses(callback_data.building)
    if not corpuses:
        await callback.answer("Нет данных по корпусам", show_alert=True)
        return

    await state.update_data(building=callback_data.building)
    await callback.answer(f"✅ Выбрано {callback_data.building}")
    await callback.message.edit_text(
        "Выбери Корпус:⤵️",
        reply_markup=build_choose_corpus(dormitory, callback_data.building),
    )
    await state.set_state(Info.corpus)


async def choose_corpus(
    callback: CallbackQuery,
    callback_data: BuildingCallback,
    state: FSMContext,
    dormitory: DormitoryRepository,
) -> None:
    if callback_data.building is None or callback_data.corpus is None:
        await callback.answer("Не выбран корпус")
        return

    floors = dormitory.get_floors(callback_data.building, callback_data.corpus)
    if not floors:
        await callback.answer("Нет данных по этажам", show_alert=True)
        return

    await state.update_data(corpus=callback_data.corpus)
    await callback.answer(f"✅ Выбрано {callback_data.corpus}")
    await callback.message.edit_text(
        "Выбери Этаж:⤵️",
        reply_markup=build_choose_floor(
            dormitory,
            callback_data.building,
            callback_data.corpus,
        ),
    )
    await state.set_state(Info.floor)


async def choose_floor(
    callback: CallbackQuery,
    callback_data: BuildingCallback,
    state: FSMContext,
) -> None:
    if (
        callback_data.building is None
        or callback_data.corpus is None
        or callback_data.floor is None
    ):
        await callback.answer("Не выбран этаж")
        return

    await state.update_data(floor=callback_data.floor)
    await callback.answer(f"✅ Выбрано {callback_data.floor}")
    await state.set_state(Info.information)
    await show_information_menu(callback, state)


async def show_information_menu(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    await callback.answer(
        f"✅ Открываю страницу с информацией для "
        f"{data['building']}-{data['corpus']}{data['floor']}..."
    )
    await callback.message.edit_text(
        text="Выбери, что ты хочешь узнать:",
        reply_markup=build_choose_information(),
    )


async def show_information(
    callback: CallbackQuery,
    callback_data: InfoCallback,
    state: FSMContext,
    dormitory: DormitoryRepository,
) -> None:
    await state.set_state(_INFO_STATES[callback_data.action])
    data = await state.get_data()

    await callback.answer(text="🕐Получаю информацию...")

    record = dormitory.get(
        building=BuildingType(data["building"]),
        corpus=CorpusType(data["corpus"]),
        floor=int(data["floor"]),
        info_type=callback_data.action,
    )

    if record is None:
        await callback.message.edit_text(
            text="Информация не найдена. Попробуй позже — данные могут ещё не обновиться.",
            reply_markup=build_info(),
        )
        return

    await callback.message.edit_text(
        text=record.text,
        parse_mode=ParseMode.HTML,
        reply_markup=build_info(),
        disable_web_page_preview=True,
    )


async def cancel_at_building(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("✅ Просмотр информации скрыт")
    await callback.message.delete()


async def back_to_building(
    callback: CallbackQuery,
    state: FSMContext,
    dormitory: DormitoryRepository,
) -> None:
    await state.set_data({})
    await callback.answer("↩️ Возвращаюсь")
    await callback.message.edit_text(
        "Выбери Общежитие:⤵️",
        reply_markup=build_choose_building(dormitory),
    )
    await state.set_state(Info.building)


async def back_to_corpus(
    callback: CallbackQuery,
    state: FSMContext,
    dormitory: DormitoryRepository,
) -> None:
    data = await state.get_data()
    building = BuildingType(data["building"])
    await state.set_data({"building": building})
    await callback.answer("↩️ Возвращаюсь")
    await callback.message.edit_text(
        "Выбери Корпус:⤵️",
        reply_markup=build_choose_corpus(dormitory, building),
    )
    await state.set_state(Info.corpus)


async def back_to_floor(
    callback: CallbackQuery,
    state: FSMContext,
    dormitory: DormitoryRepository,
) -> None:
    data = await state.get_data()
    building = BuildingType(data["building"])
    corpus = CorpusType(data["corpus"])
    await state.set_data({"building": building, "corpus": corpus})
    await callback.answer("↩️ Возвращаюсь")
    await callback.message.edit_text(
        "Выбери Этаж:⤵️",
        reply_markup=build_choose_floor(dormitory, building, corpus),
    )
    await state.set_state(Info.floor)


async def back_to_information(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(Info.information)
    await show_information_menu(callback, state)


async def cancel_flow(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.answer("✅ Просмотр информации скрыт")
    await callback.message.delete()
