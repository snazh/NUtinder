from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.exc import IntegrityError

from src.dependecies import get_user_service, get_profile_service
from src.interface.menu_texts import commands
import src.interface.keyboards as kb

from src.utils.formater import format_profile, format_anketa

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    try:
        user_service = get_user_service()
        tg_id = message.from_user.id
        await user_service.add_user(user_data={"tg_id": tg_id})
        await message.answer("Welcome message")
        await cmd_profile(message)
    except IntegrityError:
        await cmd_profile(message)
    except Exception as e:

        await message.answer(f"{e}", )
        raise Exception


@router.message(Command("profile"))
async def cmd_profile(message: Message):
    try:
        tg_id = message.from_user.id
        profile_service = get_profile_service()
        user_profile = await profile_service.get_profile_by_tg_id(tg_id=tg_id)
        if user_profile is None:
            await message.answer("Let's create your first anketa", reply_markup=kb.proceed_button)
        else:
            formatted_anketa = format_anketa(user_profile)
            await message.answer("This is how your anketa looks")
            await message.answer_photo(
                photo=user_profile["photo_url"],
                caption=formatted_anketa,
                parse_mode="Markdown",
                reply_markup=kb.account_options
            )

    except Exception as e:
        await message.answer(f"An error has occurred: {e}")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(commands.help)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(commands.other_commands)


