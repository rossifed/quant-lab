from typing import Iterable, Protocol, runtime_checkable, Callable, Awaitable
from asyncio import Queue
from dataclasses import dataclass


@runtime_checkable
class Message(Protocol):
    def __str__(self) -> str: ...


@dataclass
class MessageEnvelope:
    message: Message
    correlation_id: str | None = None
    timestamp: float | None = None


@runtime_checkable
class MessageBroker(Protocol):
    async def publish_async(self, message: Message) -> None: ...
    async def publish_many_async(self, messages: Iterable[Message]) -> None: ...


@runtime_checkable
class MessagingClient(Protocol):
    async def start(self) -> None: ...
    async def stop(self) -> None: ...


@runtime_checkable
class MessageChannel(Protocol):
    @property
    def writer(self) -> Queue[MessageEnvelope]: ...

    @property
    def reader(self) -> Queue[MessageEnvelope]: ...


@runtime_checkable
class AsyncMessageDispatcher(Protocol):
    async def publish_async(self, message: Message) -> None: ...


@runtime_checkable
class ModuleClient(Protocol):
    async def publish_async(self, message: Message) -> None: ...


@runtime_checkable
class MessageHandler(Protocol):
    """Protocol for message handlers.
    
    All message handlers must implement the handle method
    to process incoming messages.
    """
    async def handle(self, message_data: dict) -> None:
        """Handle an incoming message.
        
        Args:
            message_data: The message payload as a dictionary
        """
        ...


@runtime_checkable
class MessageConsumer(Protocol):
    """Protocol for message consumers.
    
    Generic abstraction for consuming messages from channels (topics/queues/streams).
    """
    
    def register_handler(self, channel: str, handler: Callable[[str], Awaitable[None]]) -> None:
        """Register a handler for a specific channel.
        
        Args:
            channel: The channel to consume from (topic/queue/stream)
            handler: Async function that receives raw message payload as string
        """
        ...
    
    async def consume(self) -> None:
        """Start consuming messages from all registered channels.
        
        This method should run indefinitely, dispatching messages to registered handlers.
        """
        ...


@runtime_checkable
class MessagingSettings(Protocol):
    def get_backend(self) -> str: ...
