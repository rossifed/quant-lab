from pydantic import BaseModel
from typing import Optional
from shared.messaging.protocols import MessagingSettings


class KafkaSettings(BaseModel):
    """Kafka-specific messaging settings.
    
    Explicitly implements MessagingSettings protocol for type safety.
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


# Type check: verify KafkaSettings satisfies MessagingSettings protocol
def _verify_protocol() -> None:
    """Compile-time verification that KafkaSettings implements MessagingSettings."""
    _settings: MessagingSettings = KafkaSettings(
        bootstrap_servers="test",
        topic="test", 
        group_id="test"
    )
    # If this compiles, KafkaSettings correctly implements MessagingSettings