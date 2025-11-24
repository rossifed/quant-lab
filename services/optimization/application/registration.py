from shared.di.protocols import DIContainer
from shared.logging.protocols import Logger
from shared.messaging.protocols import MessageBroker
from services.optimization.application.services.optimization_service import (
    OptimizationService,
    DummyOptimizationService
)
from services.optimization.application.handlers.backtest_handler import BacktestMessageHandler


def register_application_services(container: DIContainer) -> None:
    container.add_singleton(
        OptimizationService,# type: ignore[type-abstract]
        lambda: DummyOptimizationService(
            message_broker=container.resolve(MessageBroker),# type: ignore[type-abstract]
            logger=container.resolve(Logger)# type: ignore[type-abstract]
        )
    )
    
    # Handler registered here so it can be resolved by register_message_handler
    container.add_singleton(
        BacktestMessageHandler,
        lambda: BacktestMessageHandler(
            logger=container.resolve(Logger)# type: ignore[type-abstract]
        )
    )
