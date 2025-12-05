"""
Configuration module for llm-core service.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application settings
    app_name: str = "llm-core"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8001
    
    # Logging settings
    log_level: str = "info"
    
    # Future LLM settings (for when integrating real LLM)
    llm_model: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_max_tokens: Optional[int] = 1000
    llm_temperature: Optional[float] = 0.7
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()