from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    gemini_api_key: str = Field(..., alias="GEMINIAPI_KEY")
    HF_TOKEN: str = Field(..., alias="HF_TOKEN")

    model_config = SettingsConfigDict(env_file=".env",populate_by_name=True)

@lru_cache
def get_settings():
    return Settings()
