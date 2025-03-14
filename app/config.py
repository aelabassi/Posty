"""Load environment variables using pydantic_settings"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """ Settings class: all environment variables are validated here """
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    db_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    port: int

    class Config:
        env_file = ".env"


settings = Settings()
