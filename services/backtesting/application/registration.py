from shared.di.protocols import DIContainer
from shared.logging.protocols import Logger
from shared.messaging.protocols import MessageBroker
from services.backtesting.application.services.backtesting_service import (
    BacktestingService,
    DummyBacktestingService
)


def register_application_services(container: DIContainer) -> None:
    container.add_singleton(
        BacktestingService,# type: ignore[type-abstract]
        lambda: DummyBacktestingService(
            message_broker=container.resolve(MessageBroker),# type: ignore[type-abstract]
            logger=container.resolve(Logger)# type: ignore[type-abstract]
        )
    )
