import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session

from back.security import get_password_hash
from back.app import app
from back.database import get_session
from back.models import table_registry, User


@pytest.fixture
def client(session):

    def get_session_override():
        return session
        
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override 
        yield client 

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread':False},
        poolclass=StaticPool,

    ) 
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session 
        
    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    pwd='123456'
    user = User(username='Teste',email='teste@teste.com', password=get_password_hash('123456'))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd
    return user
    