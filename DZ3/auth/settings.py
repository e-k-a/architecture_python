from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "a=fo>k3P#M*k5X?G=kV@*g*op-r)K_iC}%=waB2_a,2EAwrLDVM)pCkz1Zvvj8_" 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    db_host: str = "db"  
    db_port: str = "5432"  
    db_name: str = "auth_db"  
    db_user: str = "postgres"
    db_password: str = "12345" 

    class Config:
        env_file = ".env"

settings = Settings()