from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
import src.interface.keyboards as kb
from src.interface.menu_texts import menu_options
from src.dependecies import get_profile_service, get_user_service, get_profile_eval_service
from src.utils.formater import format_anketa

from src.models.enums import EvalEnum

router = Router()


# Step 1: Define States
class AnketaState(StatesGroup):
    waiting_for_reaction = State()


@router.callback_query(F.data == "menu")
async def get_full_profile(callback: CallbackQuery):
    await callback.message.answer(menu_options.actions, reply_markup=kb.menu_options)


# ["1 👁️", "2 🔄", "3 🖼️", "4 ✏️", "5 🔗"]
@router.message(lambda message: message.text == "1 👁️")
async def search_anketas(message: Message, state: FSMContext):
    tg_id = message.from_user.id
    profile_service = get_profile_service()

    current_user = await profile_service.get_profile_by_tg_id(tg_id=tg_id)
    gender_enum = current_user["soulmate_gender"]
    anketas = await profile_service.get_profiles_by_gender(gender=gender_enum.value)

    # Step 2: Store the list of anketas in state data
    await state.update_data(anketas=anketas, index=0)

    # Step 3: Show the first anketa
    await show_next_anketa(message, state)


async def show_next_anketa(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data.get('index')
    anketas = data.get('anketas')

    # If no more anketas to show
    if index >= len(anketas):
        await message.answer("No more anketas available.")
        await state.clear()
        return

    anketa = anketas[index]
    formatted_anketa = format_anketa(anketa)

    # Show anketa to user
    await message.answer_photo(
        photo=anketa["photo_url"],
        caption=formatted_anketa,
        parse_mode="Markdown",
        reply_markup=kb.anketa_reaction
    )

    # Step 4: Set state to wait for user reaction
    await state.set_state(AnketaState.waiting_for_reaction)


@router.message(lambda message: message.text in ("💘", "💔", "💤"))
async def reaction_handler(message: Message, state: FSMContext):
    user_reaction = message.text
    profile_eval_service = get_profile_eval_service()
    profile_service = get_profile_service()
    data = await state.get_data()
    index = data.get('index')
    anketas = data.get('anketas')

    # Get current anketa (profile)
    anketa = anketas[index]

    eval_data = {
        "lover_id": (await profile_service.get_profile_by_tg_id(tg_id=message.from_user.id))["id"],
        "profile_id": anketa["id"]
    }

    match user_reaction:
        case "💘":
            eval_data["evaluation"] = EvalEnum["like"]
            await profile_eval_service.evaluate(eval_data)
        case "💔":
            await message.answer_sticker(
                sticker="CAACAgIAAxkBAAEIuXlkjKFfsyjbIOqVt5qFyU0Lfu5T4wACvQADrWW8F7W98z9ngTkTLwQ"
            )
            eval_data["evaluation"] = EvalEnum["dislike"]
            await profile_eval_service.evaluate(eval_data)
        case "💤":
            await message.answer("Gay")
            await state.clear()
            return

        # Move to the next anketa
    data = await state.get_data()
    index = data.get('index') + 1
    await state.update_data(index=index)

    # Show the next anketa
    await show_next_anketa(message, state)
