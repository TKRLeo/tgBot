from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import String, Integer, BigInteger, DECIMAL, ForeignKey

from src.main import engine


class Base(DeclarativeBase):
    pass

class Applicant(Base):
    __tablename__ = 'applicant'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    birthday: Mapped[str] = mapped_column(String(10))
    gender: Mapped[str] = mapped_column(String(10))
    experience: Mapped[int] = mapped_column(Integer,nullable=True)
    education: Mapped[str] = mapped_column(String(15),nullable=True)
    citizen: Mapped[str] = mapped_column(String(15), nullable=True)
    diplom: Mapped[str] = mapped_column(String(15), nullable=True)

    request_applicant = relationship("Request", back_populates="applicant_request")
    record_applicant = relationship("Record", back_populates="applicant_record")

    def __str__(self):
        return self.name

class Enterprise(Base):
    __tablename__ = 'enterprise'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(100))
    license: Mapped[str] = mapped_column(String(50))

    vacancy_enterprise = relationship('Vacancy', back_populates='enterprise_vacancy')
    def __str__(self):
        return self.name

class Vacancy(Base):
    __tablename__ = 'vacancy'
    id: Mapped[int] = mapped_column(primary_key=True)
    enterprise_id: Mapped[int] = mapped_column(ForeignKey('enterprise.id'))
    salary: Mapped[int] = mapped_column(Integer)
    age: Mapped[int] = mapped_column(Integer)
    post: Mapped[str] = mapped_column(String(50))
    education: Mapped[str] = mapped_column(String(15))
    experience: Mapped[int] = mapped_column(Integer)
    citizen: Mapped[str] = mapped_column(String(15))

    enterprise_vacancy = relationship("Enterprise",back_populates='vacancy_enterprise')
    request_vacancy = relationship("Request", back_populates='vacancy_request')

    record_vacancy = relationship("Record", back_populates="vacancy_record")
    def __str__(self):
        return self.name

class Request(Base):
    __tablename__ = 'request'
    id: Mapped[int] = mapped_column(primary_key=True)
    applicant_id: Mapped[int] = mapped_column(Integer,ForeignKey("applicant.id"),unique=True)
    vacancy_id: Mapped[int] = mapped_column(Integer,ForeignKey("vacancy.id"),unique=True)

    vacancy_request = relationship("Vacancy", back_populates='request_vacancy')
    applicant_request = relationship("Applicant", back_populates='request_applicant')

    def __str__(self):
        return self.name

class Manager(Base):
    __tablename__ = 'manager'
    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(50))
    telephone: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(10))

    record_manager = relationship("Record", back_populates="manager_record")
    def __str__(self):
        return self.name

class Record(Base):
    __tablename__ = "record"
    id: Mapped[int] = mapped_column(primary_key=True)
    vacancy_id: Mapped[int] = mapped_column(Integer,ForeignKey("vacancy.id"),unique=True)
    applicant_id: Mapped[int] = mapped_column(Integer,ForeignKey("applicant.id"),unique=True)
    manager_id: Mapped[int] = mapped_column(Integer, ForeignKey("manager.id"), unique=True)

    vacancy_record = relationship("Vacancy", back_populates="record_vacancy")
    applicant_record = relationship("Applicant", back_populates="record_applicant")
    manager_record = relationship("Manager", back_populates="record_manager")

    def __str__(self):
        return self.name


def main():
    applicants_tuples = (
        (2, 'Петрова Анна Сергеевна', '15.03.1998', 'Female', '4', 'Среднее', 'РФ', 'Бухгалтерия'),
        (3, 'Сидоров Алексей Викторович', '22.11.1995', 'Male', '3', 'Высшее', 'РФ', 'Информатика'),
        (4, 'Кузнецова Мария Андреевна', '30.05.2002', 'Female', '5', 'Высшее', 'РФ', 'Финансы'),
        (5, 'Морозов Денис Николаевич', '14.09.1990', 'Male', '2', 'Среднее', 'РФ', 'Логистика'),
        (6, 'Васильева Ольга Петровна', '11.01.1996', 'Female', '4', 'Высшее', 'РФ', 'Юриспруденция'),
        (7, 'Федоров Игорь Валерьевич', '29.08.1989', 'Male', '5', 'Высшее', 'РФ', 'Маркетинг'),
        (8, 'Соколова Елена Алексеевна', '05.12.1993', 'Female', '3', 'Среднее', 'РФ', 'Туризм'),
    )

    enterprise_tuples = (
        (1, 'Яндекс', 'г.Москва ул.Ленина', 'Имеется'),
        (2, 'Сбербанк', 'г.Москва ул.Неглинная', 'Имеется'),
        (3, 'Газпром', 'г. Санкт-Петербург ул. Грибоедова', 'Не имеется'),
        (4, 'РТС', 'г.Москва ул. Чистые пруды', 'Имеется'),
        (5, 'Ростелеком', 'г.Екатеринбург ул. Ленина', 'Не имеется'),
    )

    vacancy_tuples = (
        (1, 3, 55000, 25, 'Менеджер', 'Высшее', '5', 'РФ'),
        (2, 1, 60000, 30, 'Разработчик', 'Высшее', '4', 'РФ'),
        (3, 4, 45000, 28, 'Аналитик', 'Высшее', '3', 'РФ'),
        (4, 2, 70000, 35, 'Дизайнер', 'Высшее', '5', 'РФ'),
        (5, 5, 52000, 27, 'Маркетолог', 'Высшее', '4', 'РФ'),
    )

    manager_tuples = (
        (1,'г.Москва ул.Пушкина',7951152342,'Марцев Александр Семенович',23,'Male'),
    )
    with Session(engine) as session:
        for applicant in applicants_tuples:
            query =  Applicant(
                id = applicant[0],
                name = applicant[1],
                birthday = applicant[2],
                gender = applicant[3],
                experience = applicant[4],
                education = applicant[5],
                citizen = applicant[6],
                diplom = applicant[7]
            )
            session.add(query)
            session.commit()
        for enterprise in enterprise_tuples:
            query = Enterprise(
                id = enterprise[0],
                name = enterprise[1],
                address = enterprise[2],
                license = enterprise[3]
            )
            session.add(query)
            session.commit()
        for vacancy in vacancy_tuples:
            query = Vacancy(
                id= vacancy[0],
                enterprise_id = vacancy[1],
                salary = vacancy[2],
                age = vacancy[3],
                post = vacancy[4],
                education = vacancy[5],
                experience = vacancy[6],
                citizen = vacancy[7]
            )
            session.add(query)
            session.commit()
        for manager in manager_tuples:
            query = Manager(
                id = manager[0],
                address = manager[1],
                telephone = manager[2],
                name = manager[3],
                age = manager[4],
                gender = manager[5]
            )
            session.add(query)
            session.commit()
if __name__ == '__main__':
   main()