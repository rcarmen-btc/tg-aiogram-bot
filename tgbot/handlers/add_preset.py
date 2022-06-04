import re
import aiogram
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from tgbot.keyboards.inline_menu import menu, settings_markup
from tgbot.keyboards.add_preset_keyboard import back_date, back_to, back_from, back_name
from tgbot.keyboards.callback_datas import preset, settings, presets_list
from tgbot.misc.states import AddPreset
from tgbot.models.tgbot_db import Preset, City, Country
from tgbot.services.avia_api import AviasalesAPI
from tgbot.config import load_config
from datetime import datetime, timedelta
from tgbot.handlers.admin import back_to_menu
from db.tgbot.load_to_database import add_presets

from aiogram.types import Message, CallbackQuery, InlineQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup


from aiogram_calendar import simple_cal_callback, SimpleCalendar, dialog_cal_callback, DialogCalendar

flag = 0


async def add_preset(call: CallbackQuery):
    # await call.answer(cache_time=60)
    await call.message.edit_text("Please select START date: ", reply_markup=await DialogCalendar().start_calendar())


async def end_date(call: CallbackQuery):
    # await call.answer(cache_time=60)
    await call.message.edit_text("Please select END date: ", reply_markup=await DialogCalendar().start_calendar())


async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    global flag
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        if flag == 0:
            # await AddPreset.start_date.set()
            await state.update_data(start_date=date.strftime("%Y-%m-%d"))
            await callback_query.message.edit_text("Please select END date: ", reply_markup=await DialogCalendar().start_calendar())
            flag = 1
        else:
            await callback_query.message.edit_text('Enter origin city:', reply_markup=back_date)
            await state.update_data(end_date=date.strftime("%Y-%m-%d"))
            await AddPreset.from_enter.set()
            flag = 0


async def enter_locals(query: types.InlineQuery):
    q = query.query
    results = [
        types.InlineQueryResultArticle(
            id='img',
            title='Enter FROM local',
            description='wtf',
            input_message_content=types.InputTextMessageContent(
                message_text='wow'
            ),
        )
    ]
    if q.startswith('TO') or q.startswith('FROM'):
        if len(q.split()) == 1:
            results = [
                types.InlineQueryResultArticle(
                    id='img',
                    title='Enter TO local',
                    description='wtf',
                    input_message_content=types.InputTextMessageContent(
                        message_text='wow'
                    ),
                )
            ]
        elif len(q.split()) == 2:
            from_local = q.split()[1].title()
            counts = await City.query.limit(20).where(City.name.startswith(from_local)).gino.all()
            results = [
                types.InlineQueryResultArticle(
                    id=c.id,
                    title=c.name,
                    description=c.name,
                    input_message_content=types.InputTextMessageContent(
                        message_text=c.code
                    )
                ) for c in counts
            ]


    # if q.startswith('FROM', q):

    await query.answer(
        results=results,
        cache_time=1
    )


async def enter_to(message: types.Message, state: FSMContext):
    await state.update_data(from_local=message.text)
    await message.answer('Enter destination city:', reply_markup=back_to)
    await AddPreset.next()


async def enter_name(message: types.Message, state: FSMContext):
    await state.update_data(to_local=message.text)
    await message.answer('Enter preset name:', reply_markup=back_name)
    await AddPreset.next()


async def done(message: types.Message, state: FSMContext):

    data = await state.get_data()
    start_date = data.get('start_date')
    end_date_ = data.get('end_date')
    from_local = data.get('from_local')
    to_local = data.get('to_local')

    name = message.text

    await state.reset_state(with_data=True)
    await message.answer(f'Preset added {start_date}-{end_date_} {from_local} {to_local} {name}', reply_markup=menu)

    await add_presets(name=name, raw_query=f'{start_date}|{end_date_}|{from_local}|{to_local}')
    # config = load_config()
    # avia = AviasalesAPI(config.tg_bot.token, config.tg_bot.locale)
    # avia.prices_for_dates()
    # avia.get_latest_prices('')


async def back_hand(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='What do you want?', reply_markup=menu)
    await state.reset_state(with_data=True)


async def send_to_insta(call: CallbackQuery, callback_data: dict):
    ids = callback_data.get('id')
    preset_curr = await Preset.get(int(ids))
    start_date, end_date_, from_local, to_local = preset_curr.raw_query.split('|')
    config = load_config()
    avia = AviasalesAPI(config.tg_bot.token, config.tg_bot.locale)
    list_tick = list()
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_ = datetime.strptime(end_date_, '%Y-%m-%d')
    while start_date <= end_date_:
        list_tick.append(avia.prices_for_dates(origin=from_local, destination=to_local, departure_at=start_date.date(), return_at=None, unique=None, sorting=None, direct=None, currency=None, limit=None, page=None, one_way=None))
        start_date += timedelta(days=1)

    # avia.prices_for_dates(origin)
    # await call.message.answer(text='TRIP|' + str(list_tick[0]))


# async def send_to_insta(message: types.Message, state: FSMContext):
#     if message.text.startswith('TRIP'):
#         status, start_date, end_date_, from_local, to_local = message.text.split('|')
#         config = load_config()
#         avia = AviasalesAPI(config.tg_bot.token, config.tg_bot.locale)
#         await message.answer(str(message.text.split('|')))


def register_add_preset(dp: Dispatcher):
    dp.register_callback_query_handler(add_preset, preset.filter(method="add"))
    # dp.register_message_handler(enter_from, state=AddPreset.date_enter)
    dp.register_message_handler(enter_to, state=AddPreset.from_enter)
    dp.register_message_handler(enter_name, state=AddPreset.to_enter)
    dp.register_message_handler(done, state=AddPreset.enter_name)
    dp.register_callback_query_handler(back_hand, settings.filter(option='menu'), state=AddPreset)
    dp.register_callback_query_handler(process_dialog_calendar, dialog_cal_callback.filter())
    dp.register_inline_handler(enter_locals, state=AddPreset)
    # dp.register_callback_query_handler(send_prepear, presets_list.filter())
    dp.register_callback_query_handler(send_to_insta, presets_list.filter())
    # dp.register_message_handler(enter_from, state=AddPreset.to_enter)
