import asyncio
from aiokafka import AIOKafkaConsumer  # type: ignore
from typing import Callable, Dict, Awaitable, Any


class KafkaMessageConsumer:
    def __init__(self, consumer: AIOKafkaConsumer) -> None:
        self._consumer = consumer
        self._handlers: Dict[str, Callable[[str], Awaitable[None]]] = {}
        self._tasks: set[asyncio.Task[Any]] = set()

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
                # Launch handler without awaiting - parallel processing
                task = asyncio.create_task(self._handlers[topic](payload))  # type: ignore[arg-type]
                self._tasks.add(task)
                task.add_done_callback(self._tasks.discard)