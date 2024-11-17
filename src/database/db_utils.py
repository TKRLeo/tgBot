from sqlalchemy.exc import IntegrityError
from src.database.models import Applicant
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, delete, text
from src.config import engine
with Session(engine) as session:
    db_session = session


def is_exists(chat_id: int):
    return db_session.query(Applicant).filter(Applicant.telegram_id == chat_id).first() is not None

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