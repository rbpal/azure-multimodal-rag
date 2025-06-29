"""Azure RAG Configuration Settings"""

class AzureRAGConfig:
    """Configuration for our Azure RAG system"""
    
    # File paths
    PDF_FOLDER = "data/raw/pdfs"
    PROCESSED_FOLDER = "data/processed"
    VECTOR_STORE_FOLDER = "data/vector_store"
    LOGS_FOLDER = "logs"
    
    # Text processing settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # AI model settings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    MAX_MEMORY_GB = 8
    
    # Processing limits
    MAX_FILES_TO_PROCESS = 10
    
    # Supported file types
    SUPPORTED_FILE_TYPES = ['.pdf', '.txt', '.md']

# Global config instance
config = AzureRAGConfig()
