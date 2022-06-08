from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from tgbot.keyboards.callback_datas import presets_list
from db.tgbot.load_to_database import get_presets
from tgbot.keyboards.callback_datas import preset, settings
from aiogram import Dispatcher
from tgbot.config import load_config
from tgbot.models.tgbot_db import Preset
from tgbot.services.avia_api import AviasalesAPI
from datetime import datetime, timedelta


async def show_presets(call: CallbackQuery):
    # await call.answer(cache_time=60)
    kp = await get_presets()
    res = list()
    for i in kp:
        res.append(
            InlineKeyboardButton(
                text=i.raw_query,
                callback_data=presets_list.new(id=i.id),
            )
        )

    back_list = list()
    back_list.append(
        InlineKeyboardButton(
            text="Back to menu",
            callback_data=settings.new(option='menu'),
        ),
    )

    mass = [[i] for i in res]

    await call.message.edit_text(
        f'Presets: ',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                *mass,
                back_list
            ]
        )
    )


async def send_to_insta(call: CallbackQuery, callback_data: dict):
    ids = callback_data.get('id')
    preset_curr = await Preset.get(int(ids))
    if preset_curr is None:
        return
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
    await call.message.answer(text='TRIP|' + str(list_tick[:5]))


def register_show(dp: Dispatcher):
    dp.register_callback_query_handler(show_presets, preset.filter(method="show"))
    dp.register_callback_query_handler(send_to_insta, presets_list.filter())
