from datetime import datetime
from http import HTTPStatus

from fastapi import FastAPI,HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from back.database import get_session

from back.models import User
from back.schemas import Message, UserList, UserPublic, UserSchema,Token
from back.security import create_access_token, get_password_hash,verify_password
app = FastAPI()

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo', 'batata': 'frita'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema,session=Depends(get_session)):        
        db_user = session.scalar(
            select(User).where(
                (User.username == user.username) | (User.email == user.email)
            )
        )
        if db_user:
            if db_user.username == user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exists'

                )
                
            elif db_user.email == user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exists'

                )
        db_user = User(
             username=user.username, 
             email=user.email, 
             password=get_password_hash(user.password))
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.get('/users',response_model=UserList)
def read_users(
     limit: int = 10,
     offset: int = 0,
     session: Session = Depends(get_session)
    ):

    users = session.scalars(
         select(User).limit(limit).offset(offset)
    )
    return {'users': users}
    
@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
     user_id: int, 
     user: UserSchema,
     session:Session=Depends(get_session)
     ):



     db_user = session.scalar(          
          select(User).where(User.id == user_id)
        )
     
     if not db_user:
          raise HTTPException(
               status_code=HTTPStatus.NOT_FOUND, detail='User not found'
          )
     
     db_user.email = user.email
     db_user.username = user.username
     db_user.password = get_password_hash(user.password)
     db_user.updated_at=datetime.now()
     

     session.commit()
     session.refresh(db_user)

     return db_user
     
    
   



@app.delete('/users/{user_id}',response_model=Message)
def delete_user(user_id: int,session:Session=Depends(get_session)):

    db_user = session.scalar(          
          select(User).where(User.id == user_id)
        )
    if not db_user:          
          raise HTTPException(              
              status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        
          )
    session.delete(db_user)
    session.commit()
    return {'message': 'User deleted'}


@app.post('/token')
def login_for_access_token(
     form_data: OAuth2PasswordRequestForm = Depends(),
     session: Session=Depends(get_session)
    ):
    user = session.scalar(
         select(User).where(User.email == form_data.username)
    )
    
    if not user or not verify_password(form_data.password,user.password):
         raise HTTPException(
              status_code=400, detail= 'Incorrect email or password'
         )
    access_token = create_access_token(data={'sub': user.email})
    
    return {'access_token':access_token, 'token_type': 'Bearer'}
         
         

    