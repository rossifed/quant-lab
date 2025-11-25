from shared.di.protocols import DIContainer
from shared import register_message_handler
from services.backtesting.infrastructure.registration import register_infrastructure_services
from services.backtesting.domain.registration import register_domain_services
from services.backtesting.application.registration import register_application_services
from services.backtesting.api.registration import register_api_services
from services.backtesting.application.handlers.optimization_done_handler import OptimizationDoneHandler


def register_services(container: DIContainer) -> None:
    register_infrastructure_services(container)
    register_domain_services(container)
    register_application_services(container)
    register_api_services(container)
    
    # Register message handlers
    register_message_handler(
        channel="optimization-events",
        message_type="OptimizationDone",
        handler_class=OptimizationDoneHandler
    )
