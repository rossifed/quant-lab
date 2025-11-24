from .protocols import (
    Message,
    MessageEnvelope,
    MessageBroker,
    MessagingClient,
    MessageChannel,
    AsyncMessageDispatcher,
    ModuleClient,
    MessagingSettings,
    MessageHandler,
    MessageConsumer,
)
from .registration import add_messaging
from .message_router import MessageRouter

# Import all backend implementations to trigger auto-registration
# Each backend (kafka, redis, etc.) registers itself when imported
from . import kafka  # noqa: F401

__all__ = [
    "Message",
    "MessageEnvelope",
    "MessageBroker",
    "MessagingClient",
    "MessageChannel",
    "AsyncMessageDispatcher",
    "ModuleClient",
    "MessagingSettings",
    "MessageHandler",
    "MessageConsumer",
    "add_messaging",
    "MessageRouter",
]