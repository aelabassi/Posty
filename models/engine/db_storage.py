from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import dotenv

dotenv.load_dotenv()
SQLALCHEMY_DB_URL = os.getenv("DB_URL")
engine = create_engine(SQLALCHEMY_DB_URL)