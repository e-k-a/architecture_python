from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from schemas import UserCreate, UserDB, Token
from methods import create_access_token, create_refresh_token, get_current_user, validate_refresh_token
from db import fake_db,  get_user, get_user_by_id
from settings import settings

api_router = APIRouter()

@api_router.post("/register", response_model=UserDB)
async def register(user: UserCreate):
    if get_user(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = f"user{len(fake_db) + 1}"
    fake_db[user_id] = {
        "id": user_id,
        "email": user.email,
        "hashed_password": user.password
    }
    return UserDB(**fake_db[user_id])

@api_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or user.hashed_password != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(
        {"sub": user.id},
        timedelta(minutes=settings.access_token_expire_minutes)
    )
    refresh_token = create_refresh_token(
        {"sub": user.id},
        timedelta(days=settings.refresh_token_expire_days)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@api_router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    user_id = validate_refresh_token(refresh_token)
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    access_token = create_access_token(
        {"sub": user.id},
        timedelta(minutes=settings.access_token_expire_minutes)
    )
    new_refresh_token = create_refresh_token(
        {"sub": user.id},
        timedelta(days=settings.refresh_token_expire_days)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }

@api_router.get("/me", response_model=UserDB)
async def read_me(user: UserDB = Depends(get_current_user)):
    return user