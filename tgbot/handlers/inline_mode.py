from pprint import pprint

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import re
from aiogram.utils.markdown import hcode


def get_from_and_to(q):
    from_local = re.search(r'^\d\d-\d\d \d\d-\d\d ([^.]*)', q)
    if from_local is not None:
        from_country = re.search(r'^([^:]*)', from_local.group(1).strip()).group(0)
        from_cities_findall = re.findall(r'^[^:]*:(.*)', from_local.group(1).strip())
        from_city = ' '
        if len(from_cities_findall) > 0 and len(from_cities_findall[0]) > 0:
            from_city = from_cities_findall[0].split()[0]
        if len(from_cities_findall) == 0 or len(from_cities_findall[0]) == 0:
            title = from_country
            desc = ''
        else:
            title = from_city
            desc = f'FROM {from_country}: {from_city}'

        to_locals_findall = re.findall(r'^\d\d-\d\d \d\d-\d\d [^.]*\. (.*)', q)
        to_locals_str = ''
        to_locals_dict = {}
        if len(to_locals_findall) > 0:
            to_locals_str = to_locals_findall[0]
            to_locals = to_locals_str.split('.')
            curr_cities = []
            for to_local in to_locals:
                curr_cities = []
                curr_count = re.search(r'^[^:]*', to_local).group(0).strip()
                curr_cities_findall = re.findall(r'^[^:]*:(.*)', to_local)
                if len(curr_cities_findall) > 0:
                    curr_cities = curr_cities_findall[0].split()
                if len(curr_cities) > 0:
                    title = f'{curr_cities[-1]}'
                else:
                    title = f'{curr_count}'
                to_locals_dict[curr_count] = curr_cities
                for c in curr_cities:
                    if ':' in c:
                        return [types.InlineQueryResultArticle(
                            id='Error',
                            title='Error',
                            description='Use dots to separate countries',
                            input_message_content=types.InputTextMessageContent(
                                message_text=q,
                                parse_mode='HTML'
                            )
                        )]

            for_desc = ''
            for co in to_locals_dict:
                for_desc += f'{co}: '
                for ci in to_locals_dict[co]:
                    for_desc += f'{ci} '
                for_desc += 'AND '

            desc += f' TO {for_desc[:-4]}'

        return from_country, from_city, to_locals_dict


async def realtime_handling(query: types.InlineQuery, countries, cities):
    q = query.query
    if len(q) == 0:
        return [types.InlineQueryResultArticle(
            id='void',
            title='Example of input',
            description= '02-21 japan kano, tokyo. russia moscow. ...',
            input_message_content=types.InputTextMessageContent(
                message_text='void',
                parse_mode='HTML'
            )
        )]

    ranges = re.search(r'^(\d\d-\d\d \d\d-\d\d)', q)
    if ranges is None:
        return [types.InlineQueryResultArticle(
            id='enter date range',
            title='Just Hint',
            description='Example: 02-10 04-11 (format: dd-mm dd-mm)',
            input_message_content=types.InputTextMessageContent(
                message_text=q,
                parse_mode='HTML'
            )
        )]

    data = get_from_and_to(q)

    if data is not None and isinstance(data[0], types.InlineQueryResultArticle):
        return data

    print(data)

    if data is None:
        return [types.InlineQueryResultArticle(
            id='Enter FROM country, ":", city and dot at the end',
            title='Enter FROM country, ":", city and dot at the end',
            description='Example: Japan: Tokyo. (format: <from country>: <from city>.)',
            input_message_content=types.InputTextMessageContent(
                message_text=q,
                parse_mode='HTML'
            )
        )]

    from_country, from_city, to_locals = data

    output = matched_count = []
    for co in countries:
        if co.lower().startswith(from_country.lower()):
            matched_count.append(co)

    matched_cities = []
    if from_city != ' ':
        for city in cities[matched_count[0]]:
            if city.lower().startswith(from_city.lower()):
                matched_cities.append(city)
        output = matched_cities

    matched_to_count = []
    matched_to_cities = []
    if len(to_locals) != 0:
        for co in to_locals:
            to_count = co
        for co in countries:
            if co.lower().startswith(to_count.lower()):
                matched_to_count.append(co)
        output = matched_to_countq
        if len(to_locals[to_count]) > 0:
            for city in cities[matched_to_count[0]]:
                if city.lower().startswith(to_locals[to_count][-1].lower()):
                    matched_to_cities.append(city)
            output = matched_to_cities

    return [
        types.InlineQueryResultArticle(
            id=co,
            title=co,
            description=f'FROM {matched_count}: {matched_cities} TO {str(matched_to_count)}: {str(matched_to_cities)}',
            input_message_content=types.InputTextMessageContent(
                message_text=q,
                parse_mode='HTML'
            )
        ) for co in output
    ]


async def empty_query(query: types.InlineQuery):
    countries = [
        'Israel',
        'Russia',
        'USA',
        'France',
        'Japan',
        'Englandland',
        'Engjalkjd',
    ]
    cities = {
        'Japan': {
            'Tokyo',
            'Kyoto',
            'Osaka',
            'Kobe'
        },
        'USA': {
            'New-Yokr',
            'Washington',
            'Chicago',
        },
        'France': {
            'Paris',
            'Marsel',
        },
    }

    await query.answer(
        results=await realtime_handling(query, countries, cities),
        # cache_time=100
    )

def register_inline_mode(dp: Dispatcher):
    dp.register_inline_handler(empty_query)
