from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    LINKEDIN_ACCESS_TOKEN: str = Field(..., description="Token de acceso a la API de LinkedIn")
    DEFAULT_USER_URN: str = Field(..., description="URN del usuario por defecto")
    DEFAULT_ORGANIZATION_URN: str = Field(..., description="URN de la organización por defecto")
    DATABASE_URL: str = Field(default="sqlite+aiosqlite:///./sql_app.db", description="URL de conexión a la base de datos")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()