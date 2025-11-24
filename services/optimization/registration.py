from shared.di.protocols import DIContainer
from shared import register_message_handler
from services.optimization.infrastructure.registration import register_infrastructure_services
from services.optimization.domain.registration import register_domain_services
from services.optimization.application.registration import register_application_services
from services.optimization.api.registration import register_api_services
from services.optimization.application.handlers.backtest_handler import BacktestMessageHandler


def register_services(container: DIContainer) -> None:
    register_infrastructure_services(container)
    register_domain_services(container)
    register_application_services(container)
    register_api_services(container)
    
    # Register message handlers
    register_message_handler(
        channel="backtesting-events",
        message_type="BacktestCompletedEvent",
        handler_class=BacktestMessageHandler
    )
