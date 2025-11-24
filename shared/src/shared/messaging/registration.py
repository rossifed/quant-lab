from shared.di.protocols import DIContainer
from shared.messaging.kafka.registration import add_kafka_messaging
from shared.messaging.kafka.kafka_settings import KafkaSettings
from shared.messaging.protocols import MessagingSettings


def add_messaging(container: DIContainer, settings: MessagingSettings) -> None:
    """Register messaging services based on settings.
    
    The settings object must implement MessagingSettings protocol with get_backend() method.
    Based on the backend type, the appropriate messaging implementation is registered.
    
    Args:
        container: DI container to register services into
        settings: Messaging configuration (e.g., KafkaSettings, RabbitMQSettings)
        
    Raises:
        TypeError: If settings type doesn't match the declared backend
        NotImplementedError: If the backend is not yet supported
    """
    backend = settings.get_backend()
    
    if backend == "kafka":
        if not isinstance(settings, KafkaSettings):
            raise TypeError(
                f"Backend is 'kafka' but settings is {type(settings).__name__}, "
                f"expected KafkaSettings"
            )
        add_kafka_messaging(container, settings)
    else:
        raise NotImplementedError(
            f"Unsupported messaging backend: {backend}. "
            f"Supported backends: kafka"
        )
