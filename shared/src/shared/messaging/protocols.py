# shared/messaging/protocols.py

from typing import Iterable, Protocol, runtime_checkable
from asyncio import Queue
from dataclasses import dataclass


@runtime_checkable
class Message(Protocol):

    def __str__(self) -> str:
        ...



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
    async def start(self) -> None:
        ...

    async def stop(self) -> None:
        ...
        
@runtime_checkable
class MessageChannel(Protocol):

    @property
    def writer(self) -> Queue[MessageEnvelope]:
        ...

    @property
    def reader(self) -> Queue[MessageEnvelope]:
        ...


@runtime_checkable
class AsyncMessageDispatcher(Protocol):

    async def publish_async(self, message: Message) -> None:
        ...


@runtime_checkable
class ModuleClient(Protocol):

    async def publish_async(self, message: Message) -> None:
        ...
