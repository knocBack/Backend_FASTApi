from pydantic_settings import BaseSettings


# config file, to fetch all values from .env and dump here, into BaseSettings class
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

# initlizes settings, so that they can be used anywhere else
settings = Settings()