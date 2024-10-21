from datetime import datetime,timedelta
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo
from jwt import encode

pwd_context = PasswordHash.recommended()

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
  
 

  