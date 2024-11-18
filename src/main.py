import asyncio
from os import getenv
import re
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv
from aiogram import F
from sqlalchemy import create_engine
from keyboards.reply_kb import *
from config import *
from src.database.db_utils import db_register_user, is_exists, db_get_vacancy, db_apply_to_vacancy, db_get_applicant, \
    update_applicant_field
from src.keyboards.inline_kb import update_applicant_kb

dp = Dispatcher()
bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
class RegistrationStates(StatesGroup):
    waiting_for_registration = State()

@dp.message(CommandStart())
async def command_start(message: Message):
    await message.answer(f"Здравствуйте, <b>{message.from_user.full_name}</b>!\nВы запустили бота по поиску вакансий! Желаем удачи в поиске работы.\n",
                         reply_markup=kb_register)

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
                required_fields[key] = token[len(key) + 1:].strip().capitalize()
                break

    for key, value in required_fields.items():
        if value is None:
            await message.answer(text=f"Необходимо заполнить поле: {key}")

    birth_date_str = required_fields["Дату рождения"]

    if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', birth_date_str):
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

    await message.answer(text,reply_markup=update_applicant_kb)
    
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
async def send_applicant_info(message:Message):
    await message.answer(get_applicant(message),parse_mode = 'HTML')
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
            [InlineKeyboardButton(text='Откликнуться',callback_data=f"apply:{message.chat.id}:{vacancy.id}")]
        ])
        await message.answer(vacancies_text,reply_markup=hire_kb)


@dp.callback_query(lambda cb: cb.data.startswith("apply:"))
async def apply_to_vacancy(callback_query: CallbackQuery):
    tokens = callback_query.data.split(":")  # Извлечение id вакансии
    print(tokens)
    db_apply_to_vacancy(int(tokens[1]), int(tokens[2]))
    await callback_query.answer("Вы откликнулись на вакансию!")  # Подтверждение


@dp.callback_query(lambda c: c.data.startswith('update_'))
async def process_update_button(callback_query: CallbackQuery):
    field_map = {
        'update_name': 'name',
        'update_birthday': 'birthday',
        'update_gender': 'gender',
        'update_experience': 'experience',
        'update_education': 'education',
        'update_citizenship': 'citizen',
        'update_diploma': 'diplom',
    }

    field = field_map.get(callback_query.data)

    # Запрос нового значения от пользователя
    await bot.send_message(callback_query.from_user.id, f"Введите новое значение для {field}:")

    # Ожидание ответа
    @dp.message(lambda message: message.chat.id == callback_query.from_user.id)
    async def handle_new_value(message: Message):
        new_value = message.text
        update_applicant_field(callback_query.from_user.id, field, new_value)
        await bot.send_message(message.chat.id, f"Значение для {field} обновлено на: {new_value}")

@dp.message(F.text == "Зарегистрироваться")
async def register_user(message: Message, state: FSMContext):

    if is_exists(message.chat.id):
        await message.answer(f"У вас уже есть анкета!",reply_markup=kb_main)
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

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

