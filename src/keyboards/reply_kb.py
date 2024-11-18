from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

kb_register = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Зарегистрироваться")]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню')

kb_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Вакансии")],
    [KeyboardButton(text="Моя анкета"), KeyboardButton(text='Изменить анкету')]
], resize_keyboard=True)

