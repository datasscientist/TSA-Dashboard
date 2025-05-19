from pydantic import BaseSettings, AnyUrl, PostgresDsn, validator
from typing import List, Optional


class Settings(BaseSettings):
    # Información de la aplicación
    PROJECT_NAME: str = "MiAPI"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"

    # Configuración de Base de Datos
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str = "5432"
    DB_NAME: str
    DB_URL: Optional[PostgresDsn] = None  # Se ensambla a partir de las otras vars si no se proporciona

    # Seguridad
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Tiempo de expiración del token JWT en minutos

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyUrl] = []  # Lista de orígenes permitidos para CORS

    # Ruta al modelo de ML
    MODEL_PATH: str

    class Config:
        env_file = ".env"
        case_sensitive = True

    @validator("DB_URL", pre=True)
    def assemble_db_url(cls, v, values):
        """
        Si no se proporciona DB_URL directamente, ensamblar a partir de vars individuales.
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PASSWORD"),
            host=values.get("DB_HOST"),
            port=values.get("DB_PORT"),
            path=f"/{values.get('DB_NAME') or ''}",
        )


settings = Settings()
