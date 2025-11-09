import json
from typing import Iterable
from aiokafka import AIOKafkaProducer # type: ignore
from shared.messaging.protocols import Message, MessageBroker


class KafkaMessageBroker(MessageBroker):
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer

    async def publish_async(self, message: Message) -> None:
        await self.publish_many_async([message])

    async def publish_many_async(self, messages: Iterable[Message]) -> None:
        for message in messages:
            topic = type(message).__name__
            payload = json.dumps(message.__dict__).encode("utf-8")
            await self._producer.send_and_wait(topic, payload)
