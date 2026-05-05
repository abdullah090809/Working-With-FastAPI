from datetime import datetime, timedelta
from pickle import NONE
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.schemas.token import TokenData

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY="0ad117d0b4a4664bc2d6d813145cd3394570a4f3b3feae95b7393f82913a37c3"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=60

def Create_Access_Token(data: dict):
    payload=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp":expire})

    encoded_jwt=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def Verify_Access_Token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id=payload.get("id")
        if id is None:
            raise credentials_exception
        token_data=TokenData(**payload)
        return token_data
    except JWTError:
        raise credentials_exception

def Get_Current_User(token: str = Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate Credentials",headers={"WWW-Authenticate": "Bearer"})
    return Verify_Access_Token(token,credentials_exception)
        