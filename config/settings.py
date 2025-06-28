"""Application settings and configuration management."""

from pydantic_settings import BaseSettings  # FIXED: Correct import for Pydantic v2
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Model Configuration
    LLAMA_MODEL_PATH: str = "./models/llama-3.1-8b-q6_k.gguf"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    # LLM Backend Settings
    LLM_BACKEND: str = "mock"  # Options: "mock", "ollama", "llama-cpp"
    OLLAMA_MODEL: str = "llama3.1:8b"
    OLLAMA_URL: str = "http://localhost:11434"
    
    # Memory Management
    MAX_MEMORY_GB: int = 32
    LLAMA_CONTEXT_SIZE: int = 4096
    LLAMA_THREADS: int = 8
    
    # Vector Store
    CHROMA_PERSIST_DIR: str = "./data/vector_store"
    
    # Document Processing
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MAX_IMAGES_PER_DOCUMENT: int = 50
    
    # API Configuration
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/application.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

def ensure_directories():
    """Create required directories if they don't exist."""
    directories = [
        "models", "data/raw/pdfs", "data/processed", 
        "data/vector_store", "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

ensure_directories()
