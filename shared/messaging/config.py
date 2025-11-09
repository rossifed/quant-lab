from shared.messaging.config import MessagingSettings
from shared.messaging.kafka.config import build_messaging_client as build_kafka_client
from shared.messaging.protocols import MessagingClient


async def build_messaging_client(settings: MessagingSettings) -> MessagingClient:
    if settings.backend == "kafka":
        return await build_kafka_client(settings)

    raise NotImplementedError(f"Unsupported backend: {settings.backend}")
