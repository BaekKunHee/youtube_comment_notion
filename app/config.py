from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    YOUTUBE_API_KEY: str
    NOTION_TOKEN: str
    NOTION_DATABASE_ID: str

    class Config:
        env_file = ".env"

settings = Settings() 