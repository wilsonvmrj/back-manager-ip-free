from jwt import decode

from back.security import  create_access_token

from back.settings import Settings
settings = Settings()

def test_jwt():
    data = {
        'sub': 'test@test.com',
    }

    token = create_access_token(data)
    result = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    assert result['sub'] == data['sub']
    assert result['exp']
