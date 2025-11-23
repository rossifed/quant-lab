from shared.di.protocols import DIContainer
from shared.logging.adapter import LoggingAdapter
from shared.logging.settings import LoggingSettings
import logging


def add_logging(container: DIContainer, settings: LoggingSettings) -> None:
    logging.basicConfig(
        level=getattr(logging, settings.level),
        format=settings.format
    )
    container.add_singleton(LoggingAdapter,
                            lambda: LoggingAdapter(name=settings.app_name))