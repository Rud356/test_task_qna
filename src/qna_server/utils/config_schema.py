import tomllib
from pathlib import Path

from pydantic import BaseModel, Field


class DbSettings(BaseModel):
    connection_string: str


class AppConfig(BaseModel):
    host: str
    port: int = Field(ge=1, le=65_535)
    db_settings: DbSettings


def load_config(path: Path) -> AppConfig:
    with path.open(mode='rb') as f:
        return AppConfig(**tomllib.load(f))
