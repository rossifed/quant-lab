from pydantic import BaseSettings
from shared.messaging.protocols import MessagingClient
from shared.messaging.kafka.kafka_message_client import KafkaMessagingClient
from shared.messaging.kafka.kafka_message_broker import KafkaMessageBroker
from aiokafka import AIOKafkaProducer 


async def build_messaging_client(self) -> MessagingClient:
        if self.messaging_backend == "kafka":
            producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await producer.start()
            broker = KafkaMessageBroker(producer)
            return KafkaMessagingClient(broker)

        raise NotImplementedError("Unsupported backend")