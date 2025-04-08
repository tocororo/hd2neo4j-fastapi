from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    neo4j_uri: str
    neo4j_user: str
    neo4j_pass: str
    neo4j_db: str
    model_config = SettingsConfigDict(env_file=".env")



@lru_cache
def get_settings():
    return Settings()
