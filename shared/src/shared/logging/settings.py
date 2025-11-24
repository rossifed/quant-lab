from pydantic import BaseModel
from typing import Literal


LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LoggingSettings(BaseModel):
    app_name: str = "App"
    level: LogLevel = "INFO"
    format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
