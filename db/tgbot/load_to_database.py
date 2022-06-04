import asyncio

from tgbot.models.tgbot_db import Preset, Country, City
from tgbot.services.avia_api import AviasalesAPI
from tgbot.config import load_config
from db.tgbot.database import create_db
from sqlalchemy import select


async def get_or_crate_local(model, **kwargs):
    code = kwargs.get('code', '-1')
    instance = await model.query.where(model.code == code).gino.all()
    # inst = await model.select('code').where(model.code == code).gino.scalar()
    if not instance:
        new_preset = await model(**kwargs).create()
        print('Create record')
    else:
        print('Already exists')


async def load_countries():
    config = load_config()
    avia = AviasalesAPI(config.tg_bot.token, config.tg_bot.locale)
    print(avia)
    countries = avia.get_countries()
    if len(countries) == 0:
        print(countries)

    for country in countries:
        code = country.get('code')
        name = country.get('name')
        currency = country.get('currency')
        name_translations = str(country.get('name_translations'))
        cases = str(country.get('cases'))
        await get_or_crate_local(Country, code=code, name=name, currency=currency, name_translations=name_translations, cases=cases)


async def load_cities():
    config = load_config()
    avia = AviasalesAPI(config.tg_bot.token, config.tg_bot.locale)
    cities = avia.get_cities()
    if len(cities) == 0:
        print(cities)
    for city in cities:
        country_code = city.get('country_code')
        code = city.get('code')
        coordinates = str(city.get('coordinates'))
        name = city.get('name')
        time_zone = city.get('time_zone')
        name_translations = str(city.get('name_translations'))
        cases = str(city.get('cases'))
        await get_or_crate_local(City, country_code=country_code, code=code, coordinates=coordinates, name=name, time_zone=time_zone, name_translations=name_translations, cases=cases)


async def add_presets(**kwargs):
    await Preset(**kwargs).create()
    print('Create preset')


async def get_presets():
    instance = await Preset.query.gino.all()
    return instance


# async def
# loop = asyncio.get_event_loop()
# loop.run_until_complete(create_db())
# loop.run_until_complete(load_countries())
# loop.run_until_complete(load_cities())
