import os
import logging
from functools import lru_cache

from pydantic import BaseSettings, AnyUrl

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", False)
    database_url: AnyUrl = os.getenv("DATABASE_URL")


@lru_cache()
def get_settings():
    log.info("LOADING Environment Variables..")
    return Settings()