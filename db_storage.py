from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import dotenv
import os

dotenv.load_dotenv()
SQLALCHEMY_DB_URL = os.getenv("DB_URL")
engine = create_engine(SQLALCHEMY_DB_URL)
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()