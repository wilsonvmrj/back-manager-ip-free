from http import HTTPStatus
import json

from back.schemas import UserPublic

def create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste1',
            'password': '234234',
            'email': 'tteste@tee.com',
        },
    )



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
    assert response.json()['id'] == 1
    assert response.json()['username'] == 'teste1'
    assert response.json()['email'] ==  'tteste@tee.com'
    


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users':[]}

def test_read_users_with_user(client,user):
    user_schema = UserPublic.model_validate(user).model_dump_json()
    response = client.get('/users/')
  
  
    assert response.status_code == HTTPStatus.OK
    list_of_users= [user_schema]
    # assert response.json() == {'users': list_of_users}


def test_update_user(client,user):
    
    
    response = client.put(
        'users/1',
        json={            
        'username': 'teste1',
        'email': 'tteste@tee.com',
        'password': '123'
        }
    )

    dict_user = {
        'id':1,
        'username': 'teste1',
        'email': 'tteste@tee.com',        
    }    
    
    assert response.json()['id'] == 1
    assert response.json()['username'] == 'teste1'
    assert response.json()['email'] ==  'tteste@tee.com'
    
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



def test_delete_user(client,user):
    
    response = client.delete('/users/1')

    assert response.json() ==  {
        'message': 'User deleted'
    }

def test_delete_user_not_found(client):
    response = client.delete('/users/10')
    assert response.status_code == HTTPStatus.NOT_FOUND
    
def test_get_token(client,user):    
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.password }
    )


    token  = response.json()
    print(token)
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token





 