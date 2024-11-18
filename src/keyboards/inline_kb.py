from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

update_applicant_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить ФИО", callback_data='update_name')],
    [InlineKeyboardButton(text="Изменить дату рождения", callback_data='update_dob')],
    [InlineKeyboardButton(text="Изменить пол", callback_data='update_gender')],
    [InlineKeyboardButton(text="Изменить опыт работы", callback_data='update_experience')],
    [InlineKeyboardButton(text="Изменить образование", callback_data='update_education')],
    [InlineKeyboardButton(text="Изменить гражданство", callback_data='update_citizenship')],
    [InlineKeyboardButton(text="Изменить диплом", callback_data='update_diploma')],
    [InlineKeyboardButton(text="Сохранить изменения", callback_data='save_changes')],
    [InlineKeyboardButton(text="Отменить", callback_data='cancel')]
])