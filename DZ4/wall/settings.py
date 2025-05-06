from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8001
    DEBUG: bool = False
    
    MONGO_DB_URL: str = "mongodb://localhost:27017/"
    MONGO_DB_NAME: str = "wall_db"
    MONGO_POSTS_COLLECTION: str = "posts"
    
    class Config:
        env_file = ".env"

settings = Settings()