from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./data/stratumweb.db"
    cors_origins: str = '["http://localhost:8000"]'
    admin_password: str = "stratumweb123"

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    notification_email: str = ""

    @property
    def cors_origin_list(self) -> List[str]:
        return json.loads(self.cors_origins)

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
