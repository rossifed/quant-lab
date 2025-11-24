from shared.di.protocols import DIContainer
from shared.logging.protocols import Logger
from shared.messaging.protocols import MessageBroker
from services.optimization.application.services.optimization_service import (
    OptimizationService,
    DummyOptimizationService
)


def register_application_services(container: DIContainer) -> None:
    container.add_singleton(
        OptimizationService,
        lambda: DummyOptimizationService(
            message_broker=container.resolve(MessageBroker),
            logger=container.resolve(Logger)
        )
    )
