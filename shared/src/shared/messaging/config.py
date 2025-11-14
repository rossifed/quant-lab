
from shared.di.protocols import DIContainer
from shared.messaging.kafka.config import configure_kafka_messaging
from shared.messaging.messaging_settings import MessagingSettings   
from shared.messaging.kafka.kafka_settings import KafkaSettings

def configure_messaging(container: DIContainer, settings: MessagingSettings) -> None:
    if settings.get_backend() == "kafka":
        if isinstance(settings, KafkaSettings):
            configure_kafka_messaging(container, settings)
        else:
            raise TypeError("Expected KafkaSettings for Kafka backend")
    else:
        raise NotImplementedError(f"Unsupported backend: {settings.get_backend()}")
