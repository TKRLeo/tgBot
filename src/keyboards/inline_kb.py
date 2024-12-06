from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

update_applicant_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить ФИО", callback_data='update_applicant_name')],
    [InlineKeyboardButton(text="Изменить дату рождения", callback_data='update_applicant_dob')],
    [InlineKeyboardButton(text="Изменить пол", callback_data='update_applicant_gender')],
    [InlineKeyboardButton(text="Изменить опыт работы", callback_data='update_applicant_experience')],
    [InlineKeyboardButton(text="Изменить образование", callback_data='update_applicant_education')],
    [InlineKeyboardButton(text="Изменить гражданство", callback_data='update_applicant_citizenship')],
    [InlineKeyboardButton(text="Изменить диплом", callback_data='update_applicant_diploma')],
    [InlineKeyboardButton(text="Сохранить изменения", callback_data='update_applicant_changes')],
    [InlineKeyboardButton(text="Отменить", callback_data='update_applicant_cancel')]
])

update_vacancy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить заработную плату", callback_data='update_vacancy_salary')],
    [InlineKeyboardButton(text="Изменить возраст", callback_data='update_vacancy_age')],
    [InlineKeyboardButton(text="Изменить должность", callback_data='update_vacancy_post')],
    [InlineKeyboardButton(text="Изменить образование", callback_data='update_vacancy_education')],
    [InlineKeyboardButton(text="Изменить опыт работы", callback_data='update_vacancy_experience')],
    [InlineKeyboardButton(text="Изменить гражданство", callback_data='update_vacancy_citizen')],
    [InlineKeyboardButton(text="Сохранить изменения", callback_data='update_vacancy_changes')],
    [InlineKeyboardButton(text="Отменить", callback_data='update_vacancy_cancel')]
])

add_company_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить информацию о компании", callback_data='add_enterprise')]
])

delete_company_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Удалить",callback_data='delete_company')]
])