from http import HTTPStatus

from fastapi import FastAPI

from back.routers import auth, users, todos, vlans
from back.schemas import Message

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router )
app.include_router(vlans.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo'}
