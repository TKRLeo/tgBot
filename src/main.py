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
from aiogram.types import Message, ReplyKeyboardRemove
from dotenv import load_dotenv
from aiogram import F
from sqlalchemy import create_engine
from keyboards.reply_kb import *
from config import *
from src.database.db_utils import db_register_user, is_exists,db_get_vacancy

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
@dp.message(F.text == "Вакансии")
async def send_vacancy(message: Message):
    vacancies = db_get_vacancy()
    vacancies_text = "Список Вакансий:\n\n"

    for vacancy in vacancies:
        enterprise = vacancy.enterprise_vacancy
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
    await message.answer(vacancies_text)
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
