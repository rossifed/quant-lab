from pathlib import Path
from typing import Optional
import yaml  # type: ignore[import-untyped]
import json
from pydantic import BaseModel, Field
from shared.logging import LoggingSettings
from shared.logging.config import LoggingConfig
from shared.messaging.protocols import MessagingSettings
from shared.messaging.config import MessagingConfig


class AppSettings(BaseModel):
    """Application-level settings."""
    name: str = "service"


class AppConfig(BaseModel):
    """Root configuration model loaded from YAML/JSON.
    
    This is the only configuration the service needs to know about.
    Each subsystem (logging, messaging) knows how to parse its own section.
    """
    app: AppSettings = Field(default_factory=AppSettings)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    messaging: Optional[MessagingConfig] = None
    
    def get_logging_settings(self) -> LoggingSettings:
        """Get logging settings.
        
        Delegates to LoggingConfig which knows how to convert itself.
        """
        return self.logging.to_settings(app_name=self.app.name)
    
    def get_messaging_settings(self) -> Optional[MessagingSettings]:
        """Get messaging settings.
        
        Delegates to MessagingConfig which knows about concrete implementations.
        The service code never sees KafkaSettings, RedisSettings, etc.
        
        Returns:
            Concrete messaging settings or None if not configured
        """
        if not self.messaging:
            return None
        return self.messaging.to_settings()


def load_config(config_path: str | Path) -> AppConfig:
    """Load configuration from YAML or JSON file.
    
    The service just provides a path to config file.
    Each subsystem handles its own config parsing.
    
    Args:
        config_path: Path to configuration file (.yaml, .yml, or .json)
        
    Returns:
        AppConfig with all settings loaded and validated
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If file format is not supported or config is invalid
        
    Example:
        ```python
        # Service code - completely agnostic of implementation details!
        from pathlib import Path
        from shared import load_config, configure_services
        
        # Use Path(__file__).parent to resolve relative to main.py, not cwd
        config = load_config(Path(__file__).parent / "config.yaml")
        container = configure_services(
            logging_settings=config.get_logging_settings(),
            messaging_settings=config.get_messaging_settings()
        )
        ```
    """
    path = Path(config_path).resolve()  # Resolve to absolute path
    
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    
    # Load file based on extension
    if path.suffix in [".yaml", ".yml"]:
        with open(path, "r") as f:
            data = yaml.safe_load(f) or {}
    elif path.suffix == ".json":
        with open(path, "r") as f:
            data = json.load(f)
    else:
        raise ValueError(f"Unsupported config file format: {path.suffix}. Use .yaml, .yml, or .json")
    
    return AppConfig(**data)
