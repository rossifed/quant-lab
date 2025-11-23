from aiokafka import AIOKafkaProducer, AIOKafkaConsumer  # type: ignore
from shared.messaging.protocols import MessagingClient


class KafkaMessagingClient(MessagingClient):
    def __init__(self,
                 producer: AIOKafkaProducer, 
                 consumer: AIOKafkaConsumer) -> None:
        self._producer = producer
        self._consumer = consumer
          
    async def start(self) -> None:
        await self._producer.start()
        await self._consumer.start()

    async def stop(self) -> None:
        await self._producer.stop()
        await self._consumer.stop()