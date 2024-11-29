"""Configuration settings for the translator application."""
from typing import Dict
from pydantic_settings import BaseSettings
import json

class Settings(BaseSettings):
    """Application settings."""
    MODEL_NAME: str
    DEVICE: str
    PORT: int
    SUPPORTED_LANGUAGES: Dict[str, str]

    @classmethod
    def parse_supported_languages(cls, value: str | Dict) -> Dict[str, str]:
        """Parse the SUPPORTED_LANGUAGES environment variable."""
        if isinstance(value, dict):
            return value
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            raise ValueError("SUPPORTED_LANGUAGES must be a valid JSON object. Modify the .env file accordingly.")


    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"

settings = Settings()