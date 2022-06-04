from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from db.tgbot.load_to_database import get_presets
from tgbot.keyboards.callback_datas import preset, settings


CURRENT_LEVEL = 0
menu = InlineKeyboardMarkup(
    row_width=3,
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Show presets",
                callback_data=preset.new(method='show')
            ),
            InlineKeyboardButton(
                text="Add preset",
                callback_data=preset.new(method='add'),
            ),
            InlineKeyboardButton(
                text="Delete preset",
                callback_data=preset.new(method='remove')
            ),
        ],
        [
            InlineKeyboardButton(
                text="Settings",
                callback_data=settings.new(option='settings')
            )
        ]
    ]
)


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




