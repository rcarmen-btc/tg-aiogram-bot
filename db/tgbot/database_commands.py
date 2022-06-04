from tgbot.models.tgbot import Preset


async def add_preset(**kwargs):
    new_preset = await Preset(**kwargs).create()
    return new_preset

