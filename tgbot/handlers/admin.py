from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from tgbot.keyboards.callback_datas import preset, settings
from tgbot.keyboards.inline_menu import menu
from tgbot.keyboards.settings_keyboard import settings_markup


async def show_menu(message: types.Message, state: FSMContext):
    await message.answer(text='What do you want?', reply_markup=menu)
    await state.reset_state(with_data=True)


async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='What do you want?', reply_markup=menu)
    await state.reset_state(with_data=True)


async def remove_preset(call: CallbackQuery):
    # await call.answer(cache_time=60)
    await call.message.edit_text('Remove:', reply_markup=menu)


async def settings_hand(call: CallbackQuery):
    # await call.answer(cache_time=60)
    await call.message.edit_text('Remove:', reply_markup=settings_markup)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(show_menu, commands=["start"], state="*", is_admin=True)
    dp.register_callback_query_handler(remove_preset, preset.filter(method="remove"))
    dp.register_callback_query_handler(settings_hand, settings.filter(option='settings'))
    dp.register_callback_query_handler(back_to_menu, settings.filter(option='menu'))
