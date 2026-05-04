from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY="0ad117d0b4a4664bc2d6d813145cd3394570a4f3b3feae95b7393f82913a37c3"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def Create_Access_Token(data: dict):
    payload=data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp":expire})

    encoded_jwt=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
