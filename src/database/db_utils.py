from sqlalchemy.exc import IntegrityError
from src.database.models import Applicant, Vacancy, Enterprise, Request
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

def db_get_applicant(chat_id: int):
    return db_session.query(Applicant).filter(Applicant.telegram_id == chat_id).first()

def db_get_applicant_id(chat_id: int):
    return db_session.query(Applicant).filter(Applicant.telegram_id == chat_id).first().id

def db_apply_to_vacancy(chat_id: int, vacancy_id: int):
    query = Request(applicant_id = db_get_applicant_id(chat_id),vacancy_id = vacancy_id)
    db_session.add(query)
    db_session.commit()

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