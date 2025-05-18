from pydantic import BaseSettings

class Settings(BaseSettings):
    # FastAPI configuration settings
    PROJECT_NAME: str = "Streamlit FastAPI App"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./test.db"  # Example database URL
    SECRET_KEY: str = "your_secret_key"  # Replace with a secure key

    class Config:
        env_file = ".env"

settings = Settings()