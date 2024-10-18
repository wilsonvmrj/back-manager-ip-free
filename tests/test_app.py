from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo', 'batata': 'frita'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'password': '234234',
            'email': 'tteste@tee.com',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'teste',
        'email': 'tteste@tee.com',
    }
