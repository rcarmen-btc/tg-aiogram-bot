from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from aiogram.utils.callback_data import CallbackData
#
# settings_callback = CallbackData("st", "option")


menu = InlineKeyboardMarkup()

menu.add(
    InlineKeyboardButton(
        text="Search",
        switch_inline_query_current_chat=""
    )
)

menu.add(
    InlineKeyboardButton(
        text="Settings",
        callback_data="settings"
    )
)

# menu = InlineKeyboardMarkup(
#     row_width=2,
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(
#                 text="Search",
#                 switch_inline_query_current_chat="",
#                 callback_data="search"
#             ),
#             InlineKeyboardButton(
#                 text="Settings",
#                 switch_inline_query="",
#                 callback_data="settings"
#             )
#         ]
#     ]
# )
