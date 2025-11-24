from typing import Any
from pydantic import BaseModel
from shared.logging import LoggingSettings


class LoggingConfig(BaseModel):
    """Logging configuration.
    
    The logging module knows how to parse its own config section.
    """
    level: str = "INFO"
    format: str = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    
    def to_settings(self, app_name: str) -> LoggingSettings:
        """Convert config to LoggingSettings.
        
        Args:
            app_name: Application name from app config
            
        Returns:
            LoggingSettings instance
        """
        return LoggingSettings(
            app_name=app_name,
            level=self.level,  # type: ignore[arg-type]
            format=self.format
        )
