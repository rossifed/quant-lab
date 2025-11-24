import json
from aiokafka import AIOKafkaProducer  # type: ignore
from shared.messaging.protocols import Message, MessageBroker
from typing  import Iterable

class KafkaMessageBroker(MessageBroker):
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer

    async def publish_async(self, message: Message) -> None:
        topic = type(message).__name__
        payload = json.dumps(message.__dict__).encode("utf-8")
        await self._producer.send_and_wait(topic, payload)

    async def publish_many_async(self, messages: Iterable[Message]) -> None:
        for message in messages:
            await self.publish_async(message)