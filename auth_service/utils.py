from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
from datetime import timedelta

PWD_CTX = CryptContext(schemes=['bcrypt'], deprecated='auto')
SECRET_KEY = 'your-very-secure-secret'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def verify_password(plain_password, hashed_password):
    return PWD_CTX.verify(plain_password, hashed_password)

def hash_password(password):
    return PWD_CTX.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
