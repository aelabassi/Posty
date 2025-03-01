from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from app.oauth2 import create_access_token
import models
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

@pytest.fixture
def test_other_user(client):
    user_data = {"username": "Mxyz", "email":"Mxyz.ptlk@fiveD.inc", "password":"superman"}
    res = client.post('/users/', json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

# post fixtures
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def test_posts(test_user, test_other_user, session):
    posts_data = [{
        "title":"OpenAI lunched GPT4.5",
        "content":"OpenAI finally released their new model, me--Demian gonna test it to fight crime in Gotham",
        "user_id": test_user["id"]
    },
        {
            "title":"I will no longer be a robin",
            "content":"As you saw me in batman and robin issue 18, I abandoned my role as robin, and I will be better than my father",
            "user_id": test_user["id"]
        },
        {
            "title": "Dick days",
            "content": "Batman and robin year one story is cool narrative of Dick Grasyon--The first robin adventures.",
            "user_id": test_user["id"]
        },
        {
            "title":"Batman/Superman world finest issue 26",
            "content":"Did you saw us in that issue, it was fun!!",
            "user_id": test_other_user["id"]
        }
    ]
    posts = list(map(lambda post_data: models.Post(**post_data), posts_data))
    session.add_all(posts)
    session.commit()
    queried_posts = session.query(models.Post).all()
    return queried_posts