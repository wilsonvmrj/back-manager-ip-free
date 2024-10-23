from typing import Annotated
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from back.schemas import TodoPulic,TodoSchema
from back.database import get_session
from back.models import User
from back.security import get_current_user


router = APIRouter(prefix='/todos', tags=['todos'])

T_Session =  Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]

@router.post('/', response_model=TodoPulic)
def create_todo(
    todo: TodoSchema,
    session: T_Session,
    user: T_User,
    ):

    return todo