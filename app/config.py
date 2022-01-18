from pydantic import BaseSettings


# we can use pydantic to create env variables and config.
# it will automatically perform the necessary validation and the checks to make
# sure that env variables are getting set properly
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


settings = Settings()
