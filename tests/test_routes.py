from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schema
from app.db_storage import get_db, Base
from app.config import settings
import dotenv

dotenv.load_dotenv()

client = TestClient(app)

# route path
def test_root():
    res =  client.get("/").json()
    assert res["message"] == "Hello World"

