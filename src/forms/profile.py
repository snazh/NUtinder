from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    name = State()
    nu_id = State()
    gender = State()
    soulmate_gender = State()
    course = State()
    description = State()
    photo_url = State()
