from shared.di import DIContainer, T, Scope
from typing import Dict, Any
from typing import Type, Union, Callable


# shared/di/scope.py - ServiceScope
class ServiceScope(Scope):
    def __init__(self, container: DIContainer):
        self._instances: Dict[Type, Any] = {}
        self._container = container

    def get_or_create(self, service_type: Type[T],
                      factory: Union[Type[T], Callable]) -> T:
        """Crée ou récupère une instance dans ce scope"""
        if service_type not in self._instances:
            if callable(factory) and not isinstance(factory, type):
                # Factory function - passer le container
                self._instances[service_type] = factory(self._container)
            else:
                # Classe - instancier directement (pour les cas simples)
                self._instances[service_type] = factory()

        return self._instances[service_type]

    def clear(self) -> None:
        """Nettoie toutes les instances du scope"""
        self._instances.clear()

    def contains(self, service_type: Type) -> bool:
        """Vérifie si une instance existe dans ce scope"""
        return service_type in self._instances

    def get_instance_count(self) -> int:
        """Retourne le nombre d'instances dans ce scope"""
        return len(self._instances)