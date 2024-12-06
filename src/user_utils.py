import re
from datetime import datetime

from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram import F

from src.database.db_utils import is_exists, db_get_applicant, db_get_vacancy, db_register_user, update_applicant_field, \
    db_apply_to_vacancy
from src.keyboards.inline_kb import update_applicant_kb
from src.keyboards.reply_kb import kb_main
from src.main import dp, bot


class RegistrationStates(StatesGroup):
    waiting_for_registration = State()

class Form(StatesGroup):
    waiting_for_value = State()


@dp.message(F.text == "Войти как соискатель")
async def register_user(message: Message, state: FSMContext):
    if is_exists(message.chat.id):
        await message.answer(f"Вы успешно вошли как соискатель!",reply_markup=kb_main)
        return
    registration_text = (
        "<b>ФИО:</b>\n"
        "<b>Дату рождения:</b>\n"
        "<b>Пол:</b>\n"
        "<b>Опыт работы:</b>\n"
        "<b>Образование:</b>\n"
        "<b>Гражданство:</b>\n"
        "<b>Диплом:</b>\n"
    )
    await message.answer(f"Пожалуйста, заполните форму ниже.(Скопируйте сообщение и отправьте заполненную форму)")
    await message.answer(registration_text, parse_mode='HTML',reply_markup=kb_main)
    await state.set_state(RegistrationStates.waiting_for_registration)


@dp.message(RegistrationStates.waiting_for_registration)
async def parse_register(message: Message,state: FSMContext):
    required_fields = {
        "ФИО": None,
        "Дату рождения": None,
        "Пол": None,
        "Опыт работы": None,
        "Образование": None,
        "Гражданство": None,
        "Диплом": None
    }
    tokens = message.text.split("\n")

    for token in tokens:
        for key in required_fields.keys():
            if token.startswith(key + ":"):
                required_fields[key] = token[len(key) + 1:].strip()
                break

    for key, value in required_fields.items():
        if value is None:
            await message.answer(text=f"Необходимо заполнить поле: {key}")

    birth_date_str = required_fields["Дату рождения"]

    if not re.match(r'^\d{2}\.\d{2}\.\d{2}$', birth_date_str):
        await message.answer(text="Неверный формат 'Дата рождения'. Используйте ДД.ММ.ГГ.")
        return

    # Попытка преобразовать строку в дату
    try:
        birth_date = datetime.strptime(birth_date_str, '%d.%m.%y')
    except ValueError:
        await message.answer(text="Пожалуйста, убедитесь, что дата рождения корректна.")
        return

    try:
        experience = int(required_fields['Опыт работы'])
    except:
        await message.answer(text="Убедитесь, что вы корректно заполнили поле 'Опыт работы'")
        return

    name = required_fields["ФИО"]
    birthday = required_fields["Дату рождения"]
    gender = required_fields["Пол"]
    education = required_fields["Образование"]
    citizen = required_fields["Гражданство"]
    diplom = required_fields["Диплом"]
    chat_id = message.chat.id

    if db_register_user(name, birthday, gender, experience, education, citizen, diplom, chat_id):
        await message.answer(text="Вы успешно зарегистрировались")
    else:
        await message.answer(text="У вас уже есть анкета!")
    await state.clear()

@dp.message(F.text == 'Изменить анкету')
async def update_applicant(message: Message):
    text = get_applicant(message)

    await message.answer(text, reply_markup=update_applicant_kb)


def get_applicant(message: Message):
    id = message.chat.id

    applicant = db_get_applicant(id)

    name = applicant.name.strip()
    birthday = applicant.birthday.strip()
    gender = applicant.gender.strip()
    experience = applicant.experience
    education = applicant.education.strip()
    citizen = applicant.citizen.strip()
    diplom = applicant.diplom.strip()

    registration_text = f"""
<b>ФИО:</b> {name}
<b>Дата рождения:</b> {birthday}
<b>Пол:</b> {gender}
<b>Опыт работы:</b> {experience}
<b>Образование:</b> {education}
<b>Гражданство:</b> {citizen}
<b>Диплом:</b> {diplom}
"""

    return registration_text


@dp.message(F.text == 'Моя анкета')
async def send_applicant_info(message: Message):
    await message.answer(get_applicant(message), parse_mode='HTML')


@dp.message(F.text == "Вакансии")
async def send_vacancy(message: Message):
    vacancies = db_get_vacancy()
    await message.answer("Список Вакансий:\n\n")
    for vacancy in vacancies:
        enterprise = vacancy.enterprise_vacancy
        vacancies_text = ""
        vacancies_text += (
            f"📝 Вакансия: {vacancy.post}\n"
            f"🏢 Компания: {enterprise.name}\n"
            f"📍 Адрес: {enterprise.address}\n"
            f"💰 Зарплата: {vacancy.salary}\n"
            f"👶 Возраст: {vacancy.age} лет\n"
            f"🎓 Образование: {vacancy.education}\n"
            f"🛠️ Опыт: {vacancy.experience} лет\n"
            f"🌍 Гражданство: {vacancy.citizen}\n"
            f"🔖 Лицензия: {enterprise.license}\n"
            f"{'=' * 40}\n"
        )

        hire_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Откликнуться', callback_data=f"apply:{message.chat.id}:{vacancy.id}")]
        ])
        await message.answer(vacancies_text, reply_markup=hire_kb)

@dp.callback_query(lambda cb: cb.data.startswith("apply:"))
async def apply_to_vacancy(callback_query: CallbackQuery):
    tokens = callback_query.data.split(":")  # Извлечение id вакансии
    print(tokens)
    db_apply_to_vacancy(int(tokens[1]), int(tokens[2]))
    await callback_query.answer("Вы откликнулись на вакансию!")  # Подтверждение


@dp.callback_query(lambda c: c.data.startswith('update_applicant'))
async def process_update_button(callback_query: CallbackQuery, state: FSMContext):
    print("fdsfdsfds")
    field_map = {
        'update_applicant_name': 'name',
        'update_applicant_birthday': 'birthday',
        'update_applicant_gender': 'gender',
        'update_applicant_experience': 'experience',
        'update_applicant_education': 'education',
        'update_applicant_citizenship': 'citizen',
        'update_applicant_diploma': 'diplom',
    }


    field = field_map.get(callback_query.data)
    print(field)
    if field:

        await state.update_data(field=field)


        await bot.send_message(callback_query.from_user.id, f"Введите новое значение для {field}:")


        await state.set_state(Form.waiting_for_value)

        await callback_query.answer()



@dp.message(StateFilter(Form.waiting_for_value))
async def process_new_value(message: Message, state: FSMContext):
    user_data = await state.get_data()
    field = user_data.get('field')

    if field:

        new_value = message.text
        update_applicant_field(message.from_user.id, field, message.text)
        await bot.send_message(message.from_user.id, f"Вы обновили {field} на: {new_value}")


        await state.clear()
    else:
        await bot.send_message(message.from_user.id, "Произошла ошибка, попробуйте снова.")
