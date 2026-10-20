from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "HeliosIPS API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Variables de entorno con valores de respaldo
    DATABASE_URL: str = "postgresql://neondb_owner:npg_0fVAUa6TvPce@ep-empty-brook-b4oj5oao-pooler.c-6.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    SECRET_KEY: str = "helios_ips_clave_secreta_super_segura_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()