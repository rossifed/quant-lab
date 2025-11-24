from typing import Dict, Callable, Awaitable
from shared.messaging.protocols import MessageConsumer
import json
import asyncio


MessageHandler = Callable[[dict], Awaitable[None]]


class MessageRouter:
    """Routes messages from message channels to registered handlers based on message type.
    
    Channel is a generic concept that represents:
    - Kafka/Redpanda: topic
    - RabbitMQ: queue
    - Redis Streams: stream key
    - Azure Service Bus: topic/queue
    """
    
    def __init__(self, consumer: MessageConsumer):
        self._consumer = consumer
        # Structure: {channel: {message_type: handler}}
        self._handlers: Dict[str, Dict[str, MessageHandler]] = {}
        self._consume_task: asyncio.Task | None = None
        self._started = False
    
    def register_handler(self, channel: str, message_type: str, handler: MessageHandler) -> None:
        """Register a handler for a specific message type on a channel.
        
        Args:
            channel: The message channel to listen to (topic/queue/stream)
            message_type: The message type to handle
            handler: The async handler function
        """
        if channel not in self._handlers:
            self._handlers[channel] = {}
        self._handlers[channel][message_type] = handler
    
    async def _dispatch_message(self, channel: str, payload: str) -> None:
        """Dispatch a message to the appropriate handler."""
        message_envelope = json.loads(payload)
        message_type = message_envelope.get("message_type")
        message_data = message_envelope.get("data", {})
        
        if channel in self._handlers and message_type in self._handlers[channel]:
            await self._handlers[channel][message_type](message_data)
    
    async def start_channel(self, channel: str) -> None:
        """Start consuming from a specific channel.
        
        Args:
            channel: The message channel to start consuming from
        """
        if self._started:
            raise RuntimeError("Cannot add channels after router has started")
        
        # Create a closure to pass channel to dispatch
        async def dispatch_wrapper(payload: str) -> None:
            await self._dispatch_message(channel, payload)
        
        self._consumer.register_handler(channel, dispatch_wrapper)
    
    async def start_all(self) -> None:
        """Start consuming from all registered channels."""
        if self._started:
            return
        
        # Register all channels first
        for channel in self._handlers.keys():
            await self.start_channel(channel)
        
        # Start one consume task for all channels
        self._consume_task = asyncio.create_task(self._consumer.consume())
        self._started = True
    
    async def stop(self) -> None:
        """Stop consuming from all channels."""
        if self._consume_task:
            self._consume_task.cancel()
            try:
                await self._consume_task
            except asyncio.CancelledError:
                pass
        self._started = False
