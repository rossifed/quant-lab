# shared/dependency_injection.py
from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from typing import Type, Dict, Any, Optional, Union, Callable
from contextlib import contextmanager
import threading
from shared.di import DIContainer, T, Scope
from shared.di import ServiceScope


class DependencyInjectorContainer(DIContainer):
    def __init__(self, container: DeclarativeContainer):
        self._container = container
        self._providers: Dict[Type, Any] = {}  # Type -> Provider
        self._scoped_factories: Dict[Type, Union[Type, Callable]] = {}
        self._local = threading.local()

    def add_singleton(self, service_type: Type[T], factory: Type[T]) -> None:
        """Utilise dependency-injector pour les singletons"""
        provider = providers.Singleton(factory)
        self._providers[service_type] = provider

    def add_transient(self, service_type: Type[T], factory: Type[T]) -> None:
        """Utilise dependency-injector pour les transients"""
        provider = providers.Factory(factory)
        self._providers[service_type] = provider

    def add_scoped(self, service_type: Type[T],
                   factory: Union[Type[T], Callable[[DIContainer], T]]
                   ) -> None:
        self._scoped_factories[service_type] = factory

    def resolve(self, service_type: Type[T]) -> T:
        # 1. Services scoped - nécessitent un scope actif
        if service_type in self._scoped_factories:
            scope = self._get_current_scope()
            if scope is None:
                raise RuntimeError(f"No active scope for {service_type}")
            factory = self._scoped_factories[service_type]
            return scope.get_or_create(service_type, factory)

        # 2. Services singleton/transient - gérés par dependency-injector
        if service_type in self._providers:
            provider = self._providers[service_type]
            return provider()

        # 3. Service non enregistré
        raise Exception(f"Service not registered: {service_type}")

    def create_scope(self) -> Scope:
        """Crée un nouveau scope pour les services scoped"""
        return ServiceScope(self)

    @contextmanager
    def scope_context(self):
        """Context manager pour gérer un scope"""
        scope = self.create_scope()
        old_scope = getattr(self._local, 'current_scope', None)
        self._local.current_scope = scope
        try:
            yield scope
        finally:
            scope.clear()
            self._local.current_scope = old_scope

    def _get_current_scope(self) -> Optional[ServiceScope]:
        """Récupère le scope actuel du thread local"""
        return getattr(self._local, 'current_scope', None)

    def wire(self, modules: list[str]) -> None:
        """Wire le container dependency-injector sous-jacent"""
        try:
            self._container.wire(modules=modules)
        except Exception as e:
            print(f"⚠️ Failed to wire modules: {e}")

    # Méthodes utilitaires pour debug/inspection
    def is_registered(self, service_type: Type) -> bool:
        """Vérifie si un service est enregistré"""
        return (service_type in self._providers or
                service_type in self._scoped_factories)

    def get_registration_info(self, service_type: Type) -> Optional[str]:
        """Retourne le type d'enregistrement d'un service"""
        if service_type in self._providers:
            provider = self._providers[service_type]
            if isinstance(provider, providers.Singleton):
                return "singleton"
            elif isinstance(provider, providers.Factory):
                return "transient"
        elif service_type in self._scoped_factories:
            factory = self._scoped_factories[service_type]
            if callable(factory) and not isinstance(factory, type):
                return "scoped (factory)"
            else:
                return "scoped (class)"
        return None

    def list_registered_services(self) -> Dict[str, list]:
        """Liste tous les services enregistrés par type"""
        return {
            "singletons": [str(t) for t in self._providers.keys()
                           if isinstance(self._providers[t],
                                         providers.Singleton)],
            "transients": [str(t) for t in self._providers.keys()
                           if isinstance(self._providers[t],
                                         providers.Factory)],
            "scoped": [str(t) for t in self._scoped_factories.keys()]
        }