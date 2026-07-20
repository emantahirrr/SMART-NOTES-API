from datetime import datetime, timedelta, timezone
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
import bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGO = "HS256"
def hash_pw(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
def make_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=12)
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
def current_user(token: str = Depends(oauth2_scheme)) -> int: 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="invalid")
        return int(user_id) 
    except JWTError:
        raise HTTPException(status_code=401, detail="could not validate")