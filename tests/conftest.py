import pytest
import factory
import factory.fuzzy

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from back.app import app
from back.database import get_session
from back.models import User, Vlan, table_registry,Todo,TodoState
from back.security import get_password_hash
from back.settings import Settings

settings = Settings()

class VlanFactory(factory.Factory):
    class Meta:
        model: Vlan
    vlan=factory.Sequence(lambda n: n)
    network=factory.Sequence(lambda n: f'192.168.{n}.0')
    netmask= "255.255.255.0"
    gateway= factory.Sequence(lambda n: f'192.168.{n}.1')
    description= factory.Sequence(lambda n: f'Vlan id {n}')



class UserFactory(factory.Factory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f'test{n}')
    email= factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@123')



class TodoFactory(factory.Factory):
    class Meta: 
        model=Todo
    
    title = factory.Faker('text')
    description =factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1 



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
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = '123456'
    user = UserFactory(        
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd
    return user


@pytest.fixture
def other_user(session):
    pwd = '123456'
    user = UserFactory(        
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd
    return user




@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
