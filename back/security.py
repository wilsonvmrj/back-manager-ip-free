from datetime import datetime,timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo
from jwt import encode

from back.database import get_session


pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = 'YOU-SECRET-KEY'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str):
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password:str):
  return pwd_context.verify(plain_password,hashed_password)


def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
  )
  to_encode.update({'exp': expire})
  encode_jwt = encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

  return encode_jwt

def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
  ...
  