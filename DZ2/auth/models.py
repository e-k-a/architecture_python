from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic_settings import BaseSettings

from user_profile.models import *

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")

    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        cleaned = ''.join(c for c in v if c.isdigit() or c == '+')
        if not cleaned.startswith('+'):
            cleaned = '+' + cleaned
        return cleaned

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('email', 'phone')
    def require_email_or_phone(cls, v, values, **kwargs):
        if v is None and values.get('phone' if kwargs['field'].name == 'email' else 'email') is None:
            raise ValueError('Either email or phone must be provided')
        return v

class UserDB(UserBase):
    id: str
    hashed_password: str
    disabled: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    user_id: Optional[str] = None