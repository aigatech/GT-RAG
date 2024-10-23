import os

class Settings:
    POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost/dbname")
    NIM_API_KEY = os.getenv("NIM_API_KEY", "your_nvidia_api_key")
    PGVECTOR_DIMENSION = 1536  # Adjust based on NVIDIA nv-embed-v1 dimensions

settings = Settings()
