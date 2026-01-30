from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from TodoApp.main import app
from TodoApp.database import Base
from fastapi.testclient import TestClient
import pytest
from TodoApp.models import Todo, Users
from TodoApp.routers.auth import bycrpt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False}, poolclass=StaticPool)

TestsessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_getdb():
    db = TestsessionLocal()
    try:
        yield db
    finally:
        db.close()

def overide_get_current_user():
    return {'username':'codewithroby', 'id':1, 'user_role':'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todo(
        title='test todo',
        description='test todo description',
        priority=3,
        complete=False,
        owner_id=1
    )
    db = TestsessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        username='codewithrobytest',
        email='codewithrobytest@gmail.com',
        first_name='Eric',
        last_name='Roby',
        hashed_password=bycrpt_context.hash('testpassword'),
        role='admin',
        phone_number='(111)-111-1111'
    )
    db = TestsessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users;'))
        connection.commit()
