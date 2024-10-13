from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State

from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.dependecies import get_profile_service, get_user_service

from src.forms.profile import Register
import src.interface.keyboards as kb

from src.utils.formater import format_profile, format_anketa

from src.utils.validation import ValidationError, Validation

router = Router()


@router.callback_query(F.data == "proceed")
async def register(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Register.name)
    await callback.message.answer('Enter your name')


@router.message(Register.name)
async def enter_name(message: Message, state: FSMContext):
    try:
        await Validation.set_name(name=message.text)
        await state.update_data(name=message.text)
        await state.set_state(Register.nu_id)
        await message.answer("Enter your NU id")
    except ValidationError as e:
        await message.answer(f"{e}")


@router.message(Register.nu_id)
async def enter_nuid(message: Message, state: FSMContext):
    try:
        await Validation.set_nuid(nu_id=message.text)
        await state.update_data(nu_id=message.text)
        await state.set_state(Register.gender)
        await message.answer("Enter your gender", reply_markup=kb.gender)
    except ValidationError as e:
        await message.answer(f"{e}")


@router.message(Register.gender)
async def enter_gender(message: Message, state: FSMContext):
    try:
        gender_enum = await Validation.set_gender(gender=message.text)
        await state.update_data(gender=gender_enum)
        await state.set_state(Register.soulmate_gender)
        await message.answer("Who are you searching for?", reply_markup=kb.soulmate_gender)
    except ValidationError as e:
        await message.answer(f"{e}")


@router.message(Register.soulmate_gender)
async def enter_soulmate_gender(message: Message, state: FSMContext):
    try:
        soulmate_gender_enum = await Validation.set_soulmate_gender(gender=message.text)
        await state.update_data(soulmate_gender=soulmate_gender_enum)
        await state.set_state(Register.course)
        await message.answer("Enter your course", reply_markup=kb.course)
    except ValidationError as e:
        await message.answer(f"{e}")


@router.message(Register.course)
async def enter_course(message: Message, state: FSMContext):
    try:
        await Validation.set_course(course=message.text)
        await state.update_data(course=message.text)
        await state.set_state(Register.description)
        await message.answer("Enter description")
    except ValidationError as e:
        await message.answer(f"{e}")


@router.message(Register.description)
async def enter_desc(message: Message, state: FSMContext):
    try:
        await Validation.set_desc(desc=message.text)
        await state.update_data(description=message.text)

        await state.set_state(Register.photo_url)
        await message.answer("Enter photo")
    except ValidationError as e:
        await message.answer(f"{e}")


@router.message(Register.photo_url)
async def enter_photo(message: Message,
                      state: FSMContext
                      ):
    try:
        photo = message.photo[-1]
        await Validation.set_photo(photo_url=photo.file_id)
        photo = message.photo[-1]  # Fetching photo
        await state.update_data(photo_url=photo.file_id)

        data = await state.get_data()

    except ValidationError as e:
        await message.answer(f"{e}")

    else:
        tg_id = message.from_user.id
        profile_service = get_profile_service()
        user_service = get_user_service()

        user = await user_service.get_user_by_tg_id(tg_id)
        data["user_id"] = user["id"]

        await profile_service.create_profile(data)  # Store the profile information in database

        formatted_anketa = format_anketa(data)
        await message.answer("This is how your anketa looks")
        await message.answer_photo(
            photo=data["photo_url"],
            caption=formatted_anketa,
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
        profile_service = get_profile_service()
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


class UpdateProfileState(StatesGroup):
    waiting_for_input = State()


# Callback handler for "update_profile"
@router.callback_query(F.data == "update_profile")
async def update_profile(callback: CallbackQuery):
    await callback.message.answer("What do you want to change?", reply_markup=kb.update_profile)


# General callback handler for all update options
@router.callback_query(F.data.in_({"update_text", "update_name", "update_course", "update_photo"}))
async def handle_update_option(callback: CallbackQuery, state: FSMContext):
    update_type = callback.data

    match update_type:
        case "update_text":
            await callback.message.answer("Please enter the new text:")
        case "update_name":
            await callback.message.answer("Please enter your new name:")
        case "update_course":
            await callback.message.answer("Please enter your new course:")
        case "update_photo":

            await callback.message.answer("Please enter your new photo:")

    # Set state to wait for input, and store the type of update
    await state.update_data(update_type=update_type)
    await state.set_state(UpdateProfileState.waiting_for_input)


# General message handler to capture input and update the correct field
@router.message(UpdateProfileState.waiting_for_input)
async def handle_input(message: Message, state: FSMContext):
    try:
        # Get the stored update type from state
        data = await state.get_data()
        update_type = data['update_type']
        profile_service = get_profile_service()
        profile_id = (await profile_service.get_profile_by_tg_id(message.from_user.id))["id"]
        # Get the new value from the message
        new_value = message.text
        column: str = ""
        match update_type:
            case "update_photo":
                column = "photo_url"
                if message.photo:
                    photo = message.photo[-1]
                    photo_url = photo.file_id
                    new_value = photo_url

                else:
                    await message.answer("Please send a valid photo.")
            case "update_name":
                column = "name"

            case "update_text":
                column = "description"
        await profile_service.update_profile(profile_id=profile_id,
                                             column=column,
                                             value=new_value)


        await state.clear()
        await message.answer("Profile updated successfully")

    except Exception as e:
        await message.answer(f"{e}")
