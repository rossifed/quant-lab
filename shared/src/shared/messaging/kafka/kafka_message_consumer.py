from aiokafka import AIOKafkaConsumer  # type: ignore
from typing import Callable, Dict


class KafkaMessageConsumer:
    def __init__(self, consumer: AIOKafkaConsumer):
        self._consumer = consumer
        self._handlers: Dict[str, Callable[[str], None]] = {}

    def register_handler(self, topic: str, handler: Callable[[str], None]) -> None:
        self._handlers[topic] = handler

    async def consume(self):
        async for message in self._consumer:
            topic = message.topic
            payload = message.value.decode("utf-8")
            if topic in self._handlers:
                await self._handlers[topic](payload)
            else:
                print(f"No handler found for the topic {topic}")