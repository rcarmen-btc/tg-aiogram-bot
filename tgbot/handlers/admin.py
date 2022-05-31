from aiogram import Dispatcher
from aiogram.types import Message
from ..keyboards.inline import menu
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def admin_start(message: Message):
    await message.answer(
        text='Hello, welcome to aviasales story publisher!!!',
        reply_markup=menu
    )


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
