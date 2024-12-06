import re

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from aiogram.fsm.context import FSMContext

from src.database.db_utils import db_get_vacancy_of_manager, db_get_enterprise_by_id, db_get_vacancy_request, \
    get_vacancies_by_id, update_vacancy_field, db_add_vacancy, db_add_enterprise, is_exists, is_exists_manager, \
    db_add_manager, delete_vacancy_by_id
from src.keyboards.inline_kb import update_vacancy_kb, add_company_kb, delete_company_kb
from src.keyboards.reply_kb import kb_manager
from src.main import dp, bot
from src.user_utils import get_applicant

class RegisterManager(StatesGroup):
    waiting_form = State()
class AddVacancy(StatesGroup):
    waiting_data = State()
class AddEnterprise(StatesGroup):
    waiting_enterprise = State()
class UpdateVacancyForm(StatesGroup):
    waiting_value = State()
    vacancy_index = State()
def get_vacancies(user_id):
    return db_get_vacancy_of_manager(user_id)

@dp.message(F.text == 'Посмотреть выставленные вакансии')
async def get_vacancy_of_manager(message: Message):
    vacancies = db_get_vacancy_of_manager(message.from_user.id)
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
            f"Анкета соискателя\n"
        )
        delete_company_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Удалить", callback_data=f'delete_company_{vacancy.id}')]
        ])
        await message.answer(vacancies_text,reply_markup=delete_company_kb)

@dp.callback_query(lambda c: c.data.startswith("delete"))
async def handler_delete_vacancy(callback_query: CallbackQuery):
    print(callback_query.data.split("_"))
    index = int(callback_query.data.split("_")[2])
    if delete_vacancy_by_id(index):
       await bot.answer_callback_query(callback_query.id, text="Успешное удаление")
    else:
       await bot.answer_callback_query(callback_query.id,text="Ошибка")

@dp.message(F.text == 'Редактировать вакансии')
async def edit_vacancy(message: Message, state: FSMContext):
    vacancies = get_vacancies(message.from_user.id)
    if not vacancies:
        await message.answer("У вас нет вакансий.")
        return


    for vacancy in vacancies:
        vacancies_text = ""
        enterprise = vacancy.enterprise_vacancy
        vacancy_text = (
            f"📝 Вакансия: {vacancy.post}\n"
            f"🏢 Компания: {enterprise.name}\n"
            f"📍 Адрес: {enterprise.address}\n"
            f"💰 Зарплата: {vacancy.salary}\n"
            f"👶 Возраст: {vacancy.age} лет\n"
            f"🎓 Образование: {vacancy.education}\n"
            f"🛠️ Опыт: {vacancy.experience} лет\n"
            f"🌍 Гражданство: {vacancy.citizen}\n"
            f"🔖 Лицензия: {enterprise.license}\n"
        )


        vacancies_text += vacancy_text + "\n"


        edit_button = InlineKeyboardButton(text="Редактировать", callback_data=f"edit_{vacancy.id}")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[edit_button]])
        await message.answer(vacancies_text + "\nВыберите вакансию для редактирования:", reply_markup=keyboard)

@dp.callback_query(lambda cb: cb.data.startswith("edit_"))
async def process_edit_callback(callback_query: CallbackQuery,state:FSMContext):
    print(callback_query.data.split("_"))
    index = int(callback_query.data.split("_")[1])
    vacancy = get_vacancies_by_id(callback_query.from_user.id,index)
    await state.set_state(UpdateVacancyForm.waiting_value)
    await state.update_data(vacancy = vacancy)
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

    await callback_query.message.answer(vacancies_text, reply_markup=update_vacancy_kb)

@dp.callback_query(lambda c: c.data.startswith("update_vacancy"))
async def process_edit_vacancy(callback_query: CallbackQuery, state: FSMContext):
    field_map = {
        'update_post': 'post',
        'update_salary': 'salary',
        'update_age': 'age',
        'update_education': 'education',
        'update_experience': 'experience',
        'update_citizen': 'citizen',
    }
    print(callback_query.data)
    field = callback_query.data.split("_", 2)[-1]  # Извлекаем конкретное поле обновления
    print(field)
    field = "update_" + field
    if field in field_map:
        field_key = field_map[field]
       # await state.set_state(UpdateVacancyForm.waiting_value)
        print(await state.get_data())
        await state.update_data(field=field_key)
        await bot.answer_callback_query(callback_query.id, text=f"Введите значение для {field_key}")
    else:
        await bot.answer_callback_query(callback_query.id, text="Неизвестное поле для обновления.")
@dp.message(StateFilter(UpdateVacancyForm.waiting_value))
async def update_vacancy(message: Message, state: FSMContext):
    user_data = await state.get_data()
    field = user_data.get("field")
    vacancy = user_data.get('vacancy')
    print(f"Вакансия из состояния: {vacancy}")
    if vacancy is None:
        await message.answer("Ошибка: вакансии нет в состоянии.")
        return
    if field:
        new_value = message.text
        update_vacancy_field(message.from_user.id, new_value, field,vacancy)
    await state.clear()
@dp.message(F.text == 'Посмотреть вакансии на которые отклинулись')
async def vacancy_request(message: Message):
    vacancies = db_get_vacancy_request()
    for vacancy in vacancies:
        enterprise = db_get_enterprise_by_id(vacancy.enterprise_id)
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
            f"Анкета соискателя\n"
            f"{get_applicant(message)}"
        )

        feedback_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Одобрить', callback_data=f"apply:{message.chat.id}:{vacancy.id}")]
        ])

        await message.answer(vacancies_text,reply_markup=feedback_kb)

@dp.message(F.text == 'Добавить вакансию')
async def add_vacancy(message: Message, state: FSMContext):
    await state.set_state(AddVacancy.waiting_data)
    vacancies_text = "Скопируйте форму ниже и заполните. Отправьте сообщение с заполненной формой\n\n"
    vacancies_text += (
        f"Вакансия:\n"
        f"Компания:\n"
       # f"Адрес: \n"
        f"Зарплата:\n"
        f"Возраст:\n"
        f"Образование:\n"
        f"Опыт:\n"
        f"Гражданство:\n"
     #   f"Лицензия:"
    )
    await message.answer(text=vacancies_text)
@dp.message(AddVacancy.waiting_data)
async def handler_add_vacancy(message: Message, state: FSMContext):
    await state.update_data(form = message.text)
    required_fields = {
        "Вакансия": None,
        "Компания": None,
        "Зарплата": None,
        "Возраст": None,
        "Образование": None,
        "Опыт": None,
        "Гражданство": None,
    }
    tokens = message.text.split("\n")
    print(tokens)
    for token in tokens:
        for key in required_fields.keys():
            if token.startswith(key + ":"):
                data = token[len(key) + 1:].strip()
                required_fields[key] = None if data == "" else data

                break
    for key, value in required_fields.items():
        if value is None:
            await message.answer(text=f"Необходимо заполнить поле: {key}")
            return


    try:
        salary = float(required_fields["Зарплата"])
    except ValueError:
        await message.answer(text="Убедитесь, что вы корректно заполнили поле 'Зарплата'")
        return

    try:
        age = int(required_fields['Возраст'])
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным")
    except ValueError:
        await message.answer(text="Убедитесь, что вы корректно заполнили поле 'Возраст'")
        return


    vacancy_detail = {
        "Вакансия": required_fields["Вакансия"],
        "Компания": required_fields["Компания"],
        "Зарплата": salary,
        "Возраст": age,
        "Образование": required_fields["Образование"],
        "Опыт": required_fields["Опыт"],
        "Гражданство": required_fields["Гражданство"],
    }
    if not db_add_vacancy(message.from_user.id,vacancy_detail):
        await message.answer(text="Такой компании не существует. Сперва добавьте информацию о компании.",reply_markup=add_company_kb)
        return 

    await message.answer(text="Вакансия успешно добавлена!")

    await state.clear()
@dp.callback_query(lambda c: c.data.startswith("add_enterprise"))
async def add_enterprise(callback_query: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    text = ("Скопируйте и заполните форму, после этого отправьте сообщение:\n\n")
    text += (
        "Имя компании:\n"
        "Адресс:\n"
        "Лицензия:\n"
    )
    await state.set_state(AddEnterprise.waiting_enterprise)
    await bot.send_message(callback_query.from_user.id, text=text)


@dp.message(StateFilter(AddEnterprise.waiting_enterprise))
async def handler_enterprise(message:Message, state: FSMContext):
    required_fields = {
        "Имя компании": None,
        "Адресс": None,
        "Лицензия": None,
    }

    tokens = message.text.split("\n")


    for token in tokens:
        for field in required_fields.keys():
            if token.startswith(field):
                data = token[len(field) + 1:].strip()
                required_fields[field] = None if data == "" else data
                break


    for field, value in required_fields.items():
        if value is None:
            await message.answer(f'Пожалуйста, заполните поле: {field}')
            return


    await state.update_data(form=required_fields)


    await message.answer(
        "Спасибо! Ваша форма была успешно отправлена.\n"
        f"Данные компании:\n"
        f"Имя компании: {required_fields['Имя компании']}\n"
        f"Адресс: {required_fields['Адресс']}\n"
        f"Лицензия: {required_fields['Лицензия']}"
    )

    db_add_enterprise(required_fields)
    await state.clear()
@dp.message(F.text == 'Войти как менеджер')
async def register_manager(message:Message, state:FSMContext):
    if is_exists_manager(message.from_user.id):
        await message.answer("У вас уже есть анкета менеджера",reply_markup=kb_manager)
        return
    await message.answer(text="Прежде чем начать работу, необходимо зарегистрироваться. Для этого скопируйте ниже присланную форму для регистрации. Заполните её и отправьте нам сообщением.")
    registration_text = (
        "<b>ФИО:</b>\n"
        "<b>Возраст:</b>\n"
        "<b>Пол:</b>\n"
        "<b>Телефон:</b>\n"
        "<b>Адресс:</b>\n"
    )
    await message.answer(text = registration_text)

    await state.set_state(RegisterManager.waiting_form)

@dp.message(StateFilter(RegisterManager.waiting_form))
async def parse_manager_registration(message: Message, state: FSMContext):
    required_fields = {
        "ФИО": None,
        "Возраст": None,
        "Пол": None,
        "Телефон": None,
        "Адресс": None
    }
    tokens = message.text.split("\n")

    for token in tokens:
        for key in required_fields.keys():
            if token.startswith(key + ":"):
                data = token[len(key) + 1:].strip()
                required_fields[key] = None if data == "" else data
                break


    for key, value in required_fields.items():
        if value is None:
            await message.answer(text=f"Необходимо заполнить поле: {key}")

    age_str = required_fields["Возраст"]
    if age_str is not None and not age_str.isdigit():
        await message.answer(text="Неверный формат 'Возраст'. Используйте числовое значение.")
        return

    phone_str = required_fields["Телефон"]
    if phone_str is not None and not re.match(r'^\+?\d{10,15}$', phone_str):
        await message.answer(text="Неверный формат 'Телефон'. Используйте формат: +1234567890.")
        return

    if db_add_manager(required_fields,message.from_user.id):
        await message.answer("Вы успешно зарегистрировались")
    else:
        await message.answer("Ошибка регистрации")
    await state.clear()