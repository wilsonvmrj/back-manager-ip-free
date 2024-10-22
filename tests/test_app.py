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


def test_update_user(client,user,token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},        
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
    
def test_update_user_invalid_id_user(client,user,token):
    response = client.put(
        'users/10',
        headers={'Authorization': f'Bearer {token}'},  
        json={
            'id': user.id,
            'username': 'teste1',
            'email': 'tteste@tee.com',            
            'password': '123'
        }
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # assert response.json() == {}



def test_delete_user(client,user,token):
    
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        )

    assert response.json() ==  {
        'message': 'User deleted'
    }

def test_delete_user_not_found(client,token):
    response = client.delete(
        '/users/10',
        headers={'Authorization': f'Bearer {token}'},
        )
    assert response.status_code == 400
    assert response.json() == {'detail':'Not enough permission'}
    
def test_get_token(client,user):    
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password }
    )


    token  = response.json()    
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token

def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}



 