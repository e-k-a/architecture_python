from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class PostBase(BaseModel):
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=5000)
    is_public: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = Field(None, max_length=5000)
    is_public: Optional[bool] = None

class PostInDB(PostBase):
    id: str
    author_id: str
    created_at: datetime
    updated_at: datetime