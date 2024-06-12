from functools import lru_cache
import os
import secrets
import yaml
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, computed_field, BaseModel
from pydantic_core import MultiHostUrl


class Settings(BaseModel):
    API_V1_STR: str = "/api/v1"
    HASH_SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""
    GCP_PROJECT_ID: str
    GCP_PROJECT_LOCATION: str

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


@lru_cache
def load_settings(yml_path: str) -> Settings:
    if not yml_path or Path(yml_path).suffix != ".yml" or not Path(yml_path).exists():
        raise ValueError("Invalid file path")
    with open(file=yml_path, mode="r", encoding="utf-8") as yml_stream:
        conf = yaml.safe_load(stream=yml_stream)
        Settings.model_validate(conf, strict=True)  # type: ignore
        return Settings(**conf)


settings = load_settings(
    os.environ.get("CONFIG_PATH", Path(__file__).parent.parent / "settings.yml")
)
