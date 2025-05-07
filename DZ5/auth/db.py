

from sqlalchemy import create_engine, Column, String, Integer, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from settings import settings
from models import User

DATABASE_URL = f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def get_user(email: str, db):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()

