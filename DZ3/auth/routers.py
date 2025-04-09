from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from schemas import UserCreate, UserResponse, Token
from methods import create_access_token, create_refresh_token, get_current_user, validate_refresh_token
from db import get_db, get_user, get_user_by_id, User
from settings import settings

api_router = APIRouter()

@api_router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(user.email, db):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(id=db_user.id, email=db_user.email, hashed_password=db_user.hashed_password)

@api_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(form_data.username, db)
    if not user or user.hashed_password != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(
        {"sub": str(user.id)},
        timedelta(minutes=settings.access_token_expire_minutes)
    )
    refresh_token = create_refresh_token(
        {"sub": str(user.id)},
        timedelta(days=settings.refresh_token_expire_days)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@api_router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)): 
    user_id = validate_refresh_token(refresh_token)
    user = get_user_by_id(int(user_id), db)  
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    access_token = create_access_token(
        {"sub": str(user.id)},
        timedelta(minutes=settings.access_token_expire_minutes)
    )
    new_refresh_token = create_refresh_token(
        {"sub": str(user.id)},
        timedelta(days=settings.refresh_token_expire_days)
    )
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@api_router.get("/me", response_model=UserResponse)
async def read_me(user: User = Depends(get_current_user)):
    return UserResponse(id=user.id, email=user.email)
