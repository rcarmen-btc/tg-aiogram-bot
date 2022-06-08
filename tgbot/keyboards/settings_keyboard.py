from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tgbot.keyboards.callback_datas import settings


settings_markup = InlineKeyboardMarkup(
    row_width=3,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Add Locale",
                callback_data=settings.new(option='locale'),
            ),
            InlineKeyboardButton(
                text="Back to menu",
                callback_data=settings.new(option='menu'),
            ),
        ],
    ]
)
