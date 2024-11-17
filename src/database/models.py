from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import String, Integer, BigInteger, DECIMAL, ForeignKey


class Base(DeclarativeBase):
    pass

class Applicant(Base):
    __tablename__ = 'applicant'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,unique=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str] = mapped_column(String(50),unique=True)
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
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,unique=True)
    name: Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    address: Mapped[str] = mapped_column(String(100))
    license: Mapped[str] = mapped_column(String(50))

    vacancy_enterprise = relationship('Vacancy', back_populates='enterprise_vacancy')
    def __str__(self):
        return self.name

class Vacancy(Base):
    __tablename__ = 'vacancy'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,unique=True)
    enterprise_id: Mapped[int] = mapped_column(ForeignKey('enterprise.id'),unique=True)
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
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,unique=True)
    applicant_id: Mapped[int] = mapped_column(Integer,ForeignKey("applicant.id"),unique=True)
    vacancy_id: Mapped[int] = mapped_column(Integer,ForeignKey("vacancy.id"),unique=True)

    vacancy_request = relationship("Vacancy", back_populates='request_vacancy')
    applicant_request = relationship("Applicant", back_populates='request_applicant')

    def __str__(self):
        return self.name

class Manager(Base):
    __tablename__ = 'manager'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,unique=True)
    address: Mapped[str] = mapped_column(String(50))
    telephone: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(100),unique=True)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String(10))

    record_manager = relationship("Record", back_populates="manager_record")
    def __str__(self):
        return self.name

class Record(Base):
    __tablename__ = "record"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vacancy_id: Mapped[int] = mapped_column(Integer,ForeignKey("vacancy.id"),unique=True)
    applicant_id: Mapped[int] = mapped_column(Integer,ForeignKey("applicant.id"),unique=True)
    manager_id: Mapped[int] = mapped_column(Integer, ForeignKey("manager.id"), unique=True)

    vacancy_record = relationship("Vacancy", back_populates="record_vacancy")
    applicant_record = relationship("Applicant", back_populates="record_applicant")
    manager_record = relationship("Manager", back_populates="record_manager")

    def __str__(self):
        return self.name
