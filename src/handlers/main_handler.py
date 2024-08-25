from aiogram import Router, F

from aiogram.types import Message, CallbackQuery

import src.interface.keyboards as kb
from src.interface.menu_texts import menu_options

router = Router()


@router.callback_query(F.data == "menu")
async def get_full_profile(callback: CallbackQuery):
    await callback.message.answer(menu_options.actions, reply_markup=kb.menu_options)


@router.message(lambda message: message.text in ["1 👁️", "2 🔄", "3 🖼️", "4 ✏️", "5 🔗"])
async def handle_menu_option(message: Message):
    if message.text == "1 👁️":
        await message.answer("You selected option 1: 👁️", reply_markup=kb.anketa_reaction)

    elif message.text == "2 🔄":
        await message.answer("You selected option 2: 🔄")
    elif message.text == "3 🖼️":
        await message.answer("You selected option 3: 🖼️")
    elif message.text == "4 ✏️":
        await message.answer("You selected option 4: ✏️")
    elif message.text == "5 🔗":
        await message.answer("You selected option 5: 🔗")
