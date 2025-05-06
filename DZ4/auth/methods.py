from datetime import datetime, timedelta
from jose import jwt, JWTError
from settings import settings
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from db import get_user, get_user_by_id, get_db


def create_access_token(data: dict, expires_delta: timedelta):
    expire = datetime.now() + expires_delta
    data.update({"exp": expire})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(data: dict, expires_delta: timedelta):
    expire = datetime.now() + expires_delta
    data.update({"exp": expire, "type": "refresh"})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def validate_refresh_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise credentials_exception
        return payload.get("sub")
    except JWTError:
        raise credentials_exception
    

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(int(user_id), db) 
    if not user:
        raise credentials_exception
    return user