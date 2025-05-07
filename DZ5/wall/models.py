from pydantic import BaseModel

class TokenData(BaseModel):
    user_id: str

class UserInDB(BaseModel):
    id: str