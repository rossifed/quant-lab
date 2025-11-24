from typing import Optional, Any
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI
from shared.di.protocols import DIContainer
from shared.di.container import get_container
from shared.logging import add_logging, LoggingSettings
from shared.middleware import add_middleware
from shared.messaging import add_messaging, MessageRouter, MessageHandler
from shared.messaging.protocols import MessagingSettings, MessagingClient


_container: Optional[DIContainer] = None


def configure_services(
    container: Optional[DIContainer] = None,
    logging_settings: Optional[LoggingSettings] = None,
    messaging_settings: Optional[MessagingSettings] = None,
) -> DIContainer:
    """Configure core services (logging, messaging) in the DI container.
    
    Args:
        container: Optional DI container. If None, a new one is created.
        logging_settings: Logging configuration
        messaging_settings: Messaging configuration (e.g., KafkaSettings)
        
    Returns:
        The configured DI container
    """
    global _container
    
    if container is None:
        container = get_container()
    
    _container = container
    
    if logging_settings is None:
        logging_settings = LoggingSettings()
    add_logging(container, logging_settings)
    
    if messaging_settings:
        add_messaging(container, messaging_settings)
    
    return container


def register_app_middleware(app: FastAPI, container: DIContainer) -> None:
    """Register middleware for a FastAPI application.
    
    This should be called after configure_services() and after creating the FastAPI app.
    
    Args:
        app: The FastAPI application instance
        container: The DI container with registered services
    """
    add_middleware(app, container)


def register_message_handler(
    channel: str,
    message_type: str,
    handler_class: type[MessageHandler],
    method_name: str = "handle"
) -> None:
    """Register a handler for a specific message type on a channel.
    
    The handler class will be instantiated using the DI container,
    so all its dependencies will be automatically injected.
    
    Channel is a generic concept that represents:
    - Kafka/Redpanda: topic
    - RabbitMQ: queue
    - Redis Streams: stream key
    - Azure Service Bus: topic/queue
    
    Args:
        channel: The message channel to listen to (topic/queue/stream)
        message_type: The type of message to handle (e.g., "BacktestCompletedEvent")
        handler_class: The handler class to instantiate (must implement MessageHandler protocol)
        method_name: The method name to call on the handler (default: "handle")
    """
    if _container is None:
        raise RuntimeError(
            "Cannot register message handler: container not initialized. "
            "Call configure_services() first."
        )
    
    # Instantiate the handler using the container (with dependency injection)
    handler_instance: Any = _container.resolve(handler_class)
    handler_method = getattr(handler_instance, method_name)
    
    # Register with the message router
    message_router = _container.resolve(MessageRouter)
    message_router.register_handler(channel, message_type, handler_method)


def create_lifespan(container: DIContainer):  # type: ignore[no-untyped-def]
    """Create a lifespan context manager for FastAPI that handles messaging lifecycle.
    
    This function returns a lifespan context manager that:
    - Starts the messaging client on application startup
    - Starts the message router to consume messages
    - Properly shuts down both on application shutdown
    
    The service code doesn't need to know about the concrete messaging implementation.
    
    Args:
        container: The DI container with messaging services registered
        
    Returns:
        A lifespan context manager function for FastAPI
        
    Example:
        ```python
        from shared import configure_services, create_lifespan
        
        container = configure_services(app=app, messaging_settings=settings.get_kafka_settings())
        app.router.lifespan_context = create_lifespan(container)
        ```
    """
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        # Startup: resolve services using protocols (not concrete implementations)
        messaging_client = container.resolve(MessagingClient)  # type: ignore[type-abstract]
        message_router = container.resolve(MessageRouter)
        
        await messaging_client.start()
        await message_router.start_all()
        
        yield
        
        # Shutdown
        await message_router.stop()
        await messaging_client.stop()
    
    return lifespan
