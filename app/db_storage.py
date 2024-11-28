from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import dotenv
from .config import settings

dotenv.load_dotenv()
SQLALCHEMY_DB_URL = f'postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}'
engine = create_engine(SQLALCHEMY_DB_URL)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
