from pydantic import BaseModel
from typing import Optional, Any


class KafkaSettings(BaseModel):
    """Kafka-specific messaging settings.
    
    Explicitly implements MessagingSettings protocol for type safety.
    Registers itself in the messaging config registry.
    """
    bootstrap_servers: str
    topic: str
    group_id: str
    security_protocol: str = "PLAINTEXT"
    sasl_mechanism: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    
    def get_backend(self) -> str:
        """Return the messaging backend type.
        
        Required by MessagingSettings protocol.
        """
        return "kafka"
    
    @classmethod
    def from_config(cls, config: dict[str, Any]) -> "KafkaSettings":
        """Load KafkaSettings from config dict.
        
        Each backend knows how to parse its own configuration.
        
        Args:
            config: Raw configuration dictionary from YAML/JSON
            
        Returns:
            Validated KafkaSettings instance
        """
        return cls(**config)


# Auto-register this backend when module is imported
# Import here to avoid circular dependency (config.py imports protocols, kafka_settings imports config)
from shared.messaging.config import register_messaging_backend  # noqa: E402
register_messaging_backend("kafka", KafkaSettings.from_config)


# Type check: verify KafkaSettings satisfies MessagingSettings protocol
def _verify_protocol() -> None:
    """Compile-time verification that KafkaSettings implements MessagingSettings."""
    from shared.messaging.protocols import MessagingSettings
    _settings: MessagingSettings = KafkaSettings(
        bootstrap_servers="test",
        topic="test", 
        group_id="test"
    )
    # If this compiles, KafkaSettings correctly implements MessagingSettings