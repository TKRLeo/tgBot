from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv()
TOKEN = getenv('TOKEN')
DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_ADDRESS = getenv('DB_ADDRESS')
DB_NAME = getenv('DB_NAME')
url_db = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}'
engine = create_engine(url_db,echo = True)