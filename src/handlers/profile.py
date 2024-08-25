from aiogram import Router, F

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.dependecies import get_user_profile_service, get_user_service

from src.forms.profile import Register
import src.interface.keyboards as kb

from src.utils.formater import format_profile

from src.utils.validation import validate_data, ValidationError

router = Router()


@router.callback_query(F.data == "new_profile")
async def register(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.name)
    await callback.message.answer('Enter your name')


@router.message(Register.name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await state.set_state(Register.nu_id)
    await message.answer("Enter your NU id")


@router.message(Register.nu_id)
async def enter_nuid(message: Message, state: FSMContext):
    await state.update_data(nu_id=message.text)

    await state.set_state(Register.gender)
    await message.answer("Enter your gender", reply_markup=kb.gender)


@router.message(Register.gender)
async def enter_gender(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)

    await state.set_state(Register.soulmate_gender)
    await message.answer("Who are you searching for?", reply_markup=kb.soulmate_gender)


@router.message(Register.soulmate_gender)
async def enter_nuid(message: Message, state: FSMContext):
    await state.update_data(soulmate_gender=message.text)

    await state.set_state(Register.course)
    await message.answer("Enter your course", reply_markup=kb.course)


@router.message(Register.course)
async def enter_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)

    await state.set_state(Register.description)
    await message.answer("Enter description")


@router.message(Register.description)
async def enter_desc(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Register.photo_url)
    await message.answer("Enter photo")


@router.message(Register.photo_url)
async def enter_photo(message: Message,
                      state: FSMContext
                      ):
    try:
        photo = message.photo[-1]  # Fetching photo
        await state.update_data(photo_url=photo.file_id)

        data = await state.get_data()

        validate_data(data)

    except ValidationError as e:
        await message.answer(f"{e}. Refill anketa please")

    else:
        tg_id = message.from_user.id
        profile_service = get_user_profile_service()
        user_service = get_user_service()

        user = await user_service.get_specific_user(tg_id)
        data["user_id"] = user["id"]
        await profile_service.create_profile(data)  # Store the profile information in database
        formatted_profile = format_profile(data)
        await message.answer("This is how your anketa looks")
        await message.answer_photo(
            photo=data["photo_url"],
            caption=formatted_profile,
            parse_mode="Markdown",
            reply_markup=kb.account_options
        )
    finally:
        await state.clear()  # Clear the state


# @router.callback_query(F.data == "update_profile")
# def a():
#     pass
@router.callback_query(F.data == "details")
async def get_full_profile(callback: CallbackQuery):
    try:
        profile_service = get_user_profile_service()
        tg_id = callback.from_user.id

        profile = await profile_service.get_latest_profile(tg_id=tg_id)

        formatted_profile = format_profile(profile)

        await callback.message.answer_photo(
            photo=profile["photo_url"],
            caption=formatted_profile,
            parse_mode="Markdown"
        )
    except Exception as e:
        await callback.message.answer("An error occurred")
