from aiokafka import AIOKafkaConsumer  # type: ignore
from typing import Callable, Dict, Awaitable


class KafkaMessageConsumer:
    def __init__(self, consumer: AIOKafkaConsumer) -> None:
        self._consumer = consumer
        self._handlers: Dict[str, Callable[[str], Awaitable[None]]] = {}

    def register_handler(self, topic: str, handler: Callable[[str], Awaitable[None]]) -> None:
        self._handlers[topic] = handler
        # Update consumer subscription with all registered topics
        self._consumer.subscribe(topics=list(self._handlers.keys()))

    async def consume(self) -> None:
        async for message in self._consumer:  # type: ignore[var-annotated]
            topic = message.topic
            if message.value is None:  # type: ignore[attr-defined]
                continue
            payload: str = message.value.decode("utf-8")  # type: ignore[attr-defined]
            if topic in self._handlers:
                await self._handlers[topic](payload)  # type: ignore[arg-type]