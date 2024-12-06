from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

kb_register = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Войти как соискатель")],
    [KeyboardButton(text="Войти как менеджер")]
], resize_keyboard=True, input_field_placeholder='Выберите пункт меню')

kb_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Вакансии")],
    [KeyboardButton(text="Моя анкета"), KeyboardButton(text='Изменить анкету')]
], resize_keyboard=True)

kb_manager = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text = 'Посмотреть выставленные вакансии')],
    [KeyboardButton(text = 'Посмотреть вакансии на которые отклинулись')],
    [KeyboardButton(text = 'Редактировать вакансии')],
    [KeyboardButton(text= 'Добавить вакансию')]
],resize_keyboard=True)