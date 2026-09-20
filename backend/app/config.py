"""
MoneyFollows - Configuration Module
Centralized configuration using environment variables.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    app_env: str = Field(default="development", alias="APP_ENV")
    app_name: str = "MoneyFollows"
    app_version: str = "1.0.0"
    
    # Server
    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    frontend_url: str = Field(default="http://localhost:5173", alias="FRONTEND_URL")
    backend_url: str = Field(default="http://localhost:8000", alias="BACKEND_URL")
    
    # LLM
    llm_provider: str = Field(default="google", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gemini-2.0-flash", alias="LLM_MODEL")
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    openrouter_api_key: Optional[str] = Field(default=None, alias="OPENROUTER_API_KEY")
    google_api_key: Optional[str] = Field(default=None, alias="GOOGLE_API_KEY")
    
    # Search
    search_provider: str = Field(default="local", alias="SEARCH_PROVIDER")
    tavily_api_key: Optional[str] = Field(default=None, alias="TAVILY_API_KEY")
    serper_api_key: Optional[str] = Field(default=None, alias="SERPER_API_KEY")
    
    # Timeouts
    search_timeout: int = Field(default=30, alias="SEARCH_TIMEOUT")
    llm_timeout: int = Field(default=60, alias="LLM_TIMEOUT")
    fetch_timeout: int = Field(default=15, alias="FETCH_TIMEOUT")
    
    # Rate Limiting
    rate_limit_per_minute: int = Field(default=30, alias="RATE_LIMIT_PER_MINUTE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    def get_llm_api_key(self) -> Optional[str]:
        """Get the appropriate API key based on provider."""
        if self.llm_provider == "openai":
            return self.openai_api_key
        elif self.llm_provider == "openrouter":
            return self.openrouter_api_key
        elif self.llm_provider == "google":
            return self.google_api_key
        return None
    
    def get_search_api_key(self) -> Optional[str]:
        """Get the appropriate search API key."""
        if self.search_provider == "tavily":
            return self.tavily_api_key
        elif self.search_provider == "serper":
            return self.serper_api_key
        return None


settings = Settings()
