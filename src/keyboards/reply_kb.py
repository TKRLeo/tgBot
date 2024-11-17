from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_register = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Зарегистрироваться")]
])

kb_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Вакансии")],
    [KeyboardButton(text="Моя анкета"), KeyboardButton(text='Изменить анкету')]
])