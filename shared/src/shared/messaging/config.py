from typing import Optional, Any, Dict, Callable
from pydantic import BaseModel
from shared.messaging.protocols import MessagingSettings


# Registry of messaging backend loaders
# Each backend registers itself: {"kafka": KafkaSettings.from_config, "redis": RedisSettings.from_config}
_BACKEND_REGISTRY: Dict[str, Callable[[dict[str, Any]], MessagingSettings]] = {}


def register_messaging_backend(backend_name: str, loader: Callable[[dict[str, Any]], MessagingSettings]) -> None:
    """Register a messaging backend loader.
    
    Each messaging implementation (kafka, redis, etc.) registers itself at import time.
    
    Args:
        backend_name: Name of the backend (e.g., "kafka", "redis")
        loader: Function that takes config dict and returns MessagingSettings
        
    Example:
        ```python
        # In kafka/kafka_settings.py
        from shared.messaging.config import register_messaging_backend
        
        class KafkaSettings(BaseModel):
            ...
            @classmethod
            def from_config(cls, config: dict) -> "KafkaSettings":
                return cls(**config)
        
        # Auto-register at import time
        register_messaging_backend("kafka", KafkaSettings.from_config)
        ```
    """
    _BACKEND_REGISTRY[backend_name] = loader


class MessagingConfig(BaseModel):
    """Messaging configuration container.
    
    Uses registry pattern - each backend registers its own loader.
    No ugly if/elif chains!
    """
    backend: str
    kafka: Optional[dict[str, Any]] = None
    redis: Optional[dict[str, Any]] = None
    rabbitmq: Optional[dict[str, Any]] = None
    
    def to_settings(self) -> MessagingSettings:
        """Convert raw config dict to concrete MessagingSettings implementation.
        
        Uses the registry - each backend knows how to parse its own config.
        
        Returns:
            Concrete settings instance (KafkaSettings, etc.)
            
        Raises:
            ValueError: If backend is not configured or not registered
        """
        backend = self.backend
        
        # Get the registered loader for this backend
        loader = _BACKEND_REGISTRY.get(backend)
        if not loader:
            supported = ", ".join(_BACKEND_REGISTRY.keys()) or "none"
            raise ValueError(
                f"Unsupported messaging backend: {backend}. "
                f"Supported backends: {supported}"
            )
        
        # Get the config dict for this backend
        config_dict = getattr(self, backend, None)
        if not config_dict:
            raise ValueError(
                f"Backend '{backend}' selected but no {backend} configuration provided"
            )
        
        # Let the backend parse its own config
        return loader(config_dict)
