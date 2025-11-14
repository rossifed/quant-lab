from pydantic import BaseModel
from typing import Optional
from shared.messaging.messaging_settings import MessagingSettings
class KafkaSettings(MessagingSettings, BaseModel):
    bootstrap_servers: str
    topic: str
    group_id: str
    security_protocol: str = "PLAINTEXT"
    sasl_mechanism: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str]= None
    
    def get_backend(self) -> str:
            return "kafka"