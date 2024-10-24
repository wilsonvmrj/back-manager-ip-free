from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr
from back.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserSchemaUpdate(BaseModel):
    username: str
    email: EmailStr
    password: str
    update_at: datetime = None


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str

class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState

class TodoPulic(TodoSchema):
    id: int