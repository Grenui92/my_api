from configparser import ConfigParser
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

config = ConfigParser()
config.read('config.ini')

db_login = config.get('DB', 'login')
db_pass = config.get('DB', 'pass')
db_host = config.get('DB', 'host')
db_port = config.get('DB', 'port')
db_name = config.get('DB', 'db_name')


SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{db_login}:{db_pass}@{db_host}:{db_port}/{db_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
