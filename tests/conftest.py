from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from app.main import app
from app.db_storage import get_db, Base
from app.config import settings
import pytest
import dotenv

dotenv.load_dotenv()

# db connection

SQLALCHEMY_DB_URL = f'postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}_test'
engine = create_engine(SQLALCHEMY_DB_URL)

TestSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)



# fixtures
@pytest.fixture
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides = {get_db: override_get_db}
    yield TestClient(app)

# user fixtures
@pytest.fixture
def test_user(client):
    user_data = {"username": "Robin", "email":"Damian.wyne@batfam.inc", "password":"kingrobin"}
    res = client.post('/users/', json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
