from http import HTTPStatus

from fastapi import FastAPI

from back.schemas import Message, UserDB, UserList, UserPublic, UserSchema

database = []


app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo', 'batata': 'frita'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())
    database.append(user_with_id)

    return user_with_id

@app.get('/users',response_model=UserList)
def read_users():
    return {'users': database}
    