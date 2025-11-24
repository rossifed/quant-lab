from shared.di.protocols import DIContainer
from services.optimization.infrastructure.registration import register_infrastructure_services
from services.optimization.domain.registration import register_domain_services
from services.optimization.application.registration import register_application_services
from services.optimization.api.registration import register_api_services


def register_services(container: DIContainer) -> None:
    register_infrastructure_services(container)
    register_domain_services(container)
    register_application_services(container)
    register_api_services(container)
