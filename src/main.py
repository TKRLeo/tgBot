from os import getenv


from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, BigInteger, DECIMAL, ForeignKey
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_ADDRESS = getenv('DB_ADDRESS')
DB_NAME = getenv('DB_NAME')
url = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}'
engine = create_engine(url,echo = True)
