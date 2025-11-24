from typing import Dict, Any, Type, Callable
from shared.di.protocols import DIContainer, T, Scope


class ServiceScope(Scope):
    def __init__(self, container: DIContainer):
        self._instances: Dict[Type[Any], Any] = {}

    def get_or_create(self, service_type: Type[T],
                      factory: Callable[[], T]) -> T:
        if service_type not in self._instances:
            self._instances[service_type] = factory()
        return self._instances[service_type]

    def clear(self) -> None:
        self._instances.clear()

    def contains(self, service_type: Type[Any]) -> bool:
        return service_type in self._instances

    def get_instance_count(self) -> int:
        return len(self._instances)