import os

from pydantic_settings import BaseSettings, SettingsConfigDict

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, '.env')


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(  # configuring .env file
        env_file=env_path,
        env_file_encoding='utf-8',
        extra="ignore")  # ignoring other secret keys)


class DBSettings(CoreSettings):
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?async_fallback=True"


class BotSettings(CoreSettings):
    BOT_TOKEN: str


class S3BucketSettings(CoreSettings):
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_S3_BUCKET_NAME: str
    AWS_REGION: str
    AWS_ENDPOINT_URL: str


db_settings = DBSettings()
bot_settings = BotSettings()
s3bucket_settings = S3BucketSettings()