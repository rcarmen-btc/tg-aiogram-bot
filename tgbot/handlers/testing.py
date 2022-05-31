from aiogram import types, Dispatcher
from ..misc.states import Test
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from aiogram.types import Message


async def enter_testing(message: Message):
    await message.answer("Hello, r u a gey?!")
    await Test.q1.set()


async def answ_q1(message: Message, state: FSMContext):
    answ = message.text

    # await state.update_data(answ1=answ)
    async with state.proxy() as storage:
        storage["answ1"] = answ
    #     storage["answ1"].append("Hello")

    await message.answer("Y r u a gey?!")
    await Test.next()


async def answ_q2(message: Message, state: FSMContext):
    data = await state.get_data()
    answ2 = message.text

    await state.update_data(answ2=answ2)
    # async with state.proxy() as storage:
    #     storage["answ1"] = answ
    #     storage["answ1"].append("Hello")
    if data['answ1'] in ('yes', 'yep', 'yooo'):
        await message.answer(f"Y r u a gey?! U anwrd {data['answ1']}")
    else:
        await message.answer(f"Y r u a gey?!")
    await state.reset_state(with_data=False)


def register_test(dp: Dispatcher):
    dp.register_message_handler(enter_testing, commands=["test"])
    dp.register_message_handler(answ_q1, state=Test.q1)
    dp.register_message_handler(answ_q2, state=Test.q2)
