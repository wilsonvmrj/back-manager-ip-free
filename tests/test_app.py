from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste1',
            'password': '234234',
            'email': 'tteste@tee.com',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'teste1',
        'email': 'tteste@tee.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users':[
        {
        'id': 1,
        'username': 'teste1',
        'email': 'tteste@tee.com',
        },
    ]}


def test_update_user(client):
    response = client.put(
        'users/1',
        json={
             'id': 1,
        'username': 'teste1',
        'email': 'tteste@tee.com',
        'password': '123'
        }
    )
    assert response.json() == {
            'id': 1,
        'username': 'teste1',
        'email': 'tteste@tee.com',
    }
def test_update_user_invalid_id_user(client):
    response = client.put(
        'users/10',
        json={
             'id': 1,
        'username': 'teste1',
        'email': 'tteste@tee.com',
        'password': '123'
        }
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {
        'detail': 'User not found'
    }



def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() ==  {
        'message': 'User deleted'
    }

def test_delete_user_not_found(client):
    response = client.delete('/users/10')
    assert response.status_code == HTTPStatus.NOT_FOUND
    