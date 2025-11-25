from shared.di.protocols import DIContainer
from shared.logging.protocols import Logger
from shared.messaging.protocols import MessageBroker
from services.optimization.application.services.optimization_service import (
    OptimizationService,
    RayOptimizationService
)
from services.optimization.application.handlers.backtest_sliced_handler import BacktestSlicedHandler


def register_application_services(container: DIContainer) -> None:
    container.add_singleton(
        OptimizationService,  # type: ignore[type-abstract]
        lambda: RayOptimizationService(
            message_broker=container.resolve(MessageBroker),  # type: ignore[type-abstract]
            logger=container.resolve(Logger)  # type: ignore[type-abstract]
        )
    )
    
    # Register message handlers for DI resolution
    container.add_transient(
        BacktestSlicedHandler,
        lambda: BacktestSlicedHandler(
            optimization_service=container.resolve(OptimizationService)  # type: ignore[type-abstract]
        )
    )
