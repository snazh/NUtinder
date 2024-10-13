from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# main = ReplyKeyboardMarkup(keyboard=[
#     [KeyboardButton(text="Create a profile")],
#     [KeyboardButton(text="Change photo")],
#     [KeyboardButton(text="I am done")],
#
# ], resize_keyboard=True, input_field_placeholder="Choose smth...")

account_options = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text="Details", callback_data="details")],
    [InlineKeyboardButton(text="Change smth", callback_data="update_profile")],
    [InlineKeyboardButton(text="Deactivate", callback_data="deactivate")],
    [InlineKeyboardButton(text="Menu", callback_data="menu")]
])

menu_options = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="1 👁️")],
    [KeyboardButton(text="2 🔄")],
    [KeyboardButton(text="3 🖼️")],
    [KeyboardButton(text="4 ✏️")],
    [KeyboardButton(text="5 🔗")]
], resize_keyboard=True)

anketa_reaction = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="💘")],
    [KeyboardButton(text="💔")],
    [KeyboardButton(text="💤")]
], resize_keyboard=True, input_field_placeholder="???")
gender = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="female")],
    [KeyboardButton(text="male")],
    [KeyboardButton(text="other")],

], resize_keyboard=True, input_field_placeholder="What is your gender?")

soulmate_gender = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="female")],
    [KeyboardButton(text="male")],
    [KeyboardButton(text="all")],

], resize_keyboard=True, input_field_placeholder="Who are you searching?")

course = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="NUFYP")],
    [KeyboardButton(text="1st course")],
    [KeyboardButton(text="2nd course")],
    [KeyboardButton(text="3rd course")],
    [KeyboardButton(text="4th course")],
    [KeyboardButton(text="Master degree")],
    [KeyboardButton(text="PhD degree")],

], resize_keyboard=True, input_field_placeholder="Your course?")

proceed_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="proceed", callback_data="proceed")],
])


update_profile = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text="Photo", callback_data="update_photo")],
    [InlineKeyboardButton(text="Text", callback_data="update_text")],
    [InlineKeyboardButton(text="Name", callback_data="update_name")],
    [InlineKeyboardButton(text="Course", callback_data="update_course")]
])
