from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from src.dependecies import get_user_service, get_user_profile_service
from src.interface.menu_texts import commands
import src.interface.keyboards as kb

from src.utils.formater import format_profile, format_anketa

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_service = get_user_service()
    profile_service = get_user_profile_service()

    tg_id = message.from_user.id

    try:

        user_profile = await profile_service.get_latest_profile(tg_id=tg_id)

        if user_profile is None:
            await message.answer("Let's create your first anketa", reply_markup=kb.proceed_button)
            await user_service.add_user(tg_id=tg_id)
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
        await message.answer("An error occurred")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(commands.help)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await message.answer(commands.other_commands)

# @router.callback_query(F.data == "profile")
# async def create_profile(callback: CallbackQuery, state: FSMContext):
#     await state.set_state(Register.name)
#     await callback.message.answer('Enter your name')
