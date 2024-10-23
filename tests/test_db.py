from sqlalchemy import select

from back.models import User


def test_create_user(session):
    user = User(
        username='Wilson',
        email='wilson.magalhaes@gmail.com',
        password='minha_senha_legal',
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'wilson.magalhaes@gmail.com')
    )
    assert result.username == 'Wilson'
    assert result.id == 1
