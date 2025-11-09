from aiokafka import AIOKafkaProducer
from shared.messaging.kafka.kafka_message_broker import KafkaMessageBroker
from shared.messaging.kafka.kafka_message_client import KafkaMessagingClient
from shared.messaging.protocols import MessagingClient
from shared.messaging.config import MessagingSettings  # ✅ type exact


async def build_messaging_client(settings: MessagingSettings) -> MessagingClient:
    producer = AIOKafkaProducer(bootstrap_servers=settings.bootstrap_servers)
    await producer.start()
    broker = KafkaMessageBroker(producer)
    client = KafkaMessagingClient(broker, producer)
    await client.start()
    return client
