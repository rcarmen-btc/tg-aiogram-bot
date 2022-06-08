from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from tgbot.keyboards.callback_datas import preset, settings

back_from = InlineKeyboardMarkup(
    row_width=3,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Back to menu",
                callback_data=settings.new(option='menu'),
            ),
            InlineKeyboardButton(
                text="Hints",
                # callback_data=settings.new(option='menu'),
                switch_inline_query_current_chat='FROM '
            ),
        ],
    ]
)

back_to = InlineKeyboardMarkup(
    row_width=3,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Back to menu",
                callback_data=settings.new(option='menu'),
            ),
            InlineKeyboardButton(
                text="Hints",
                # callback_data=settings.new(option='menu'),
                switch_inline_query_current_chat='TO '
            ),
        ],
    ]
)

back_name = InlineKeyboardMarkup(
    row_width=3,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Back to menu",
                callback_data=settings.new(option='menu'),
            ),
        ],
    ]
)
