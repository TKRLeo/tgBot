from sqlalchemy.exc import IntegrityError
from src.database.models import Applicant, Vacancy, Enterprise, Request, Manager
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete, text
from src.config import engine
with Session(engine) as session:
    db_session = session


def is_exists(chat_id: int):
    return db_session.query(Applicant).filter(Applicant.telegram_id == chat_id).first() is not None

def db_get_vacancy():
    return db_session.query(Vacancy).join(Enterprise).all()
def db_get_vacancy_request():
    return db_session.query(Vacancy).join(Request,Vacancy.id == Request.vacancy_id).all()
def db_get_vacancy_of_manager(chat_id: int):
    manager = db_session.query(Manager).filter(Manager.telegram_id == chat_id).first()
    manager_id = manager.id
    return db_session.query(Vacancy).filter(Vacancy.manager_id == manager_id).join(Enterprise).all()
def db_get_applicant(chat_id: int):
    return db_session.query(Applicant).filter(Applicant.telegram_id == chat_id).first()

def db_get_applicant_id(chat_id: int):
    return db_session.query(Applicant).filter(Applicant.telegram_id == chat_id).first().id

def db_apply_to_vacancy(chat_id: int, vacancy_id: int):
    query = Request(applicant_id = db_get_applicant_id(chat_id),vacancy_id = vacancy_id)
    db_session.add(query)
    db_session.commit()

def db_get_enterprise_by_id(enterprise_id: int):
    return db_session.query(Enterprise).filter(Enterprise.id == enterprise_id).first()
def update_applicant_field(user_id, field, new_value):
    applicant = db_session.query(Applicant).filter(Applicant.telegram_id == user_id).first()

    if applicant is None:
        raise ValueError(f"Претендент с ID {user_id} не найден.")

    if field == 'name':
        applicant.name = new_value
    elif field == 'birthday':
        applicant.birthday = new_value
    elif field == 'gender':
        applicant.gender = new_value
    elif field == 'experience':
        applicant.experience = new_value
    elif field == 'education':
        applicant.education = new_value
    elif field == 'citizen':
        applicant.citizen = new_value
    elif field == 'diplom':
        applicant.diplom = new_value
    else:
        raise ValueError(f"Неизвестное поле: {field}")

    db_session.commit()

def db_register_user(name: str, birthday: str, gender: str, experience: int, education: str,
                     citizen: str, diplom: str,chat_id : int):
    try:

        query = Applicant(name=name, birthday=birthday, gender=gender,
                          experience=experience, education=education, citizen=citizen, diplom=diplom,telegram_id = chat_id)

        db_session.add(query)
        db_session.commit()
        return True

    except IntegrityError:
        db_session.rollback()
        return False
def get_vacancies_by_id(chat_id: int, vacancy_id: int):
    return db_session.query(Vacancy).join(Enterprise).filter(Vacancy.id == vacancy_id).first()

def update_vacancy_field(chat_id: int, new_value, attribute,vacancy):
    if attribute == 'post':
        vacancy.post = new_value
    elif attribute == 'salary':
        vacancy.salary = new_value
    elif attribute == 'age':
        vacancy.age = new_value
    elif attribute == 'education':
        vacancy.education = new_value
    elif attribute == 'experience':
        vacancy.experience = new_value
    elif attribute == 'citizen':
        vacancy.citizen = new_value
    else:
        raise ValueError(f"Не удалось обновить поле: {attribute}")

    db_session.commit()

def db_get_manager_id(chat_id: int):
    return db_session.query(Manager).filter(Manager.telegram_id == chat_id).first().id
def db_add_vacancy(chat_id: int, vacancy_detail):
    manager_id = db_get_manager_id(chat_id)
    try:
        enterprise_id = db_session.query(Enterprise).filter(Enterprise.name == vacancy_detail['Компания']).first().id
    except AttributeError:
        return False
    try:
        query = Vacancy(post = vacancy_detail['Вакансия'], enterprise_id = enterprise_id, manager_id=manager_id, salary = vacancy_detail['Зарплата'],
                        age=vacancy_detail['Возраст'], education = vacancy_detail['Образование'], experience = vacancy_detail['Опыт'],
                        citizen = vacancy_detail['Гражданство'])

        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        return False

def db_add_enterprise(details):
    try:
        query = Enterprise(name = details['Имя компании'], address=details['Адресс'], license=details['Лицензия'])
        db_session.add(query)
        db_session.commit()
    except IntegrityError:
        raise ValueError

def is_exists_manager(telegram_id: int):
    return db_session.query(Manager).filter(Manager.telegram_id == telegram_id).first() is not None

def db_add_manager(details,id):
    try:
        query = Manager(name = details['ФИО'], age = details['Возраст'], gender = details['Пол'], telephone = details['Телефон']
                        ,address = details['Адресс'],telegram_id = id)
        db_session.add(query)
        db_session.commit()
        return True
    except IntegrityError:
        return False
def delete_vacancy_by_id(vacancy_id: int):
    try:
        vacancy = db_session.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
        if vacancy:
            db_session.delete(vacancy)
            db_session.commit()
            return True
        return False
    except IntegrityError:
        db_session.rollback()
        return False

