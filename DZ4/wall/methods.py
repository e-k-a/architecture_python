from datetime import datetime, timedelta
from jose import jwt, JWTError
from settings import settings

from fastapi import Depends, HTTPException, status
from models import TokenData
from uuid import uuid4
from typing import Dict
from schemas import PostInDB
import pymongo 
import os 
mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongo:27017/wall_db")
client = pymongo.MongoClient(mongo_uri)
db = client.get_default_database() 

posts_collection = db[settings.MONGO_POSTS_COLLECTION]

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
    
    post_dict = new_post.dict()
    post_dict["_id"] = post_dict.pop("id")
    posts_collection.insert_one(post_dict)
    
    return new_post

def get_post(post_id: str):
    post_data = posts_collection.find_one({"_id": post_id})
    if post_data:
        post_data["id"] = post_data.pop("_id")
        return PostInDB(**post_data)
    return None

def get_posts(skip: int = 0, limit: int = 10, author_id: str = None):
    query = {}
    if author_id:
        query["author_id"] = author_id
    
    cursor = posts_collection.find(query).sort("created_at", pymongo.DESCENDING).skip(skip).limit(limit)
    
    posts = []
    for post_data in cursor:
        post_data["id"] = post_data.pop("_id")
        posts.append(PostInDB(**post_data))
    return posts

def update_post(post_id: str, update_data: dict):
    update_data["updated_at"] = datetime.now()
    result = posts_collection.update_one(
        {"_id": post_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        return None
    
    updated_post = posts_collection.find_one({"_id": post_id})
    if updated_post:
        updated_post["id"] = updated_post.pop("_id")
        return PostInDB(**updated_post)
    return None

def delete_post(post_id: str):
    result = posts_collection.delete_one({"_id": post_id})
    return result.deleted_count > 0

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