from datetime import datetime, timedelta
from jose import jwt, JWTError
from settings import settings

from fastapi import Depends, HTTPException, status
from models import TokenData
from uuid import uuid4
from typing import Dict
from schemas import PostInDB

posts_db: Dict[str, PostInDB] = {}

def create_post(post_data: dict, author_id: str):
    post_id = str(uuid4())
    now = datetime.now()
    
    new_post = PostInDB(
        id=post_id,
        author_id=author_id,
        created_at=now,
        updated_at=now,
        **post_data
    )
    
    posts_db[post_id] = new_post
    return new_post

def get_post(post_id: str):
    return posts_db.get(post_id)

def get_posts(skip: int = 0, limit: int = 10, author_id: str = None):
    posts = list(posts_db.values())
    
    if author_id:
        posts = [p for p in posts if p.author_id == author_id]
    
    posts.sort(key=lambda p: p.created_at, reverse=True)
    return posts[skip:skip + limit]

def update_post(post_id: str, update_data: dict):
    post = posts_db[post_id]
    updated_post = post.copy(update=update_data)
    updated_post.updated_at = datetime.now()
    posts_db[post_id] = updated_post
    return updated_post

def delete_post(post_id: str):
    del posts_db[post_id]

def create_access_token(data: dict, expires_delta: timedelta):
    expire = datetime.now() + expires_delta
    data.update({"exp": expire})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(data: dict, expires_delta: timedelta):
    expire = datetime.now() + expires_delta
    data.update({"exp": expire, "type": "refresh"})
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

async def get_token_data(authorization: str):
    print("authorization", authorization)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            authorization,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        print("payload", payload)
        user_id: str = payload.get("sub")
        print("user_id",user_id)
        if user_id is None:
            raise credentials_exception
        return TokenData(user_id=user_id)
    except (JWTError, IndexError):
        raise credentials_exception

async def get_current_user(token_data: TokenData = Depends(get_token_data)):
    print("token_data",token_data)
    return {"id": token_data.user_id}