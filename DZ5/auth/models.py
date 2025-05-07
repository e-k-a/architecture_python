from sqlalchemy import  Column, String, Integer, Index
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  
    email = Column(String, unique=True, index=True)    
    hashed_password = Column(String)

    __table_args__ = (
        Index('ix_users_email', 'email', unique=True),  
    )