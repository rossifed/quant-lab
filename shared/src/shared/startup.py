from typing import Optional
from fastapi import FastAPI
from shared.di.protocols import DIContainer
from shared.di.container import get_container
from shared.logging import add_logging, LoggingSettings
from shared.middleware import add_middleware
from shared.messaging import add_messaging
from shared.messaging.protocols import MessagingSettings


def configure_services(
    container: Optional[DIContainer] = None,
    app: Optional[FastAPI] = None,
    logging_settings: Optional[LoggingSettings] = None,
    messaging_settings: Optional[MessagingSettings] = None,
) -> DIContainer:
    if container is None:
        container = get_container()
    
    if logging_settings is None:
        logging_settings = LoggingSettings()
    add_logging(container, logging_settings)
    
    if messaging_settings:
        add_messaging(container, messaging_settings)
    
    if app:
        add_middleware(app, container)
    
    return container
