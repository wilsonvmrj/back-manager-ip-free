from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter,Depends
from fastapi.exceptions import  HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from back.database import get_session
from back.models import User, Todo
from back.schemas import Message, TodoList, TodoPublic,TodoSchema
from back.security import get_current_user


router = APIRouter(prefix='/todos', tags=['todos'])

T_Session =  Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]

@router.post('/', response_model=TodoPublic)
def create_todo(
    todo: TodoSchema,
    session: T_Session,
    user: T_CurrentUser,
    ):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        state=todo.state,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo

@router.get('/',response_model=TodoList)
def list_todos(
    session: T_Session,
    user: T_CurrentUser,
    title: str | None = None,
    descrition: str | None = None,
    state: str | None = None,
    offset: int | None = None,
    limit: int | None = None,
    ):
    query = select(Todo).where(Todo.user_id == user.id)

    if title:
        query = query.filter(Todo.title.contains(title))
    
    if descrition:
        query = query.filter(Todo.description.contains(descrition))
    if state:
        query = query.filter(Todo.state == state)
    
    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}

@router.delete('/{todo_id}', response_model=Message)
def delete_todo(
    todo_id: int,
    session: T_Session,
    user: T_CurrentUser,    
):
    todo = session.scalar(
        select(Todo).where(Todo.user_id == user.id,Todo.id== todo_id)        
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND
        )
    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully'}


    

