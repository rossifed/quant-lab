from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers
from typing import Type, Dict, Any, Optional, Union, Callable, Generator
from contextlib import contextmanager
import threading
from shared.di.protocols import DIContainer, T, Scope, ServiceNotRegisteredError
from shared.di.scope import ServiceScope


class DIContainerAdapter(DIContainer):
    def __init__(self, container: DeclarativeContainer):
        self._container = container
        self._providers: Dict[Type[Any], Any] = {}
        self._scoped_factories: Dict[Type[Any], Union[Type[Any], Callable[..., Any]]] = {}
        self._local = threading.local()

    def add_singleton(self, service_type: Type[T], provider: Union[Callable[[], T], T]) -> None:
        if callable(provider):
            provider_instance = providers.Singleton(provider)  # type: ignore[arg-type]
        else:
            provider_instance = providers.Singleton(lambda: provider)  # type: ignore[arg-type, return-value]
        self._providers[service_type] = provider_instance

    def add_transient(self, service_type: Type[T], provider: Callable[[], T]) -> None:
        provider_instance = providers.Factory(provider)
        self._providers[service_type] = provider_instance

    def add_scoped(self, service_type: Type[T],
                   provider: Callable[[], T]
                   ) -> None:
        self._scoped_factories[service_type] = provider

    def resolve(self, service_type: Type[T]) -> T:
        if service_type in self._scoped_factories:
            scope = self._get_current_scope()
            if scope is None:
                raise RuntimeError(f"No active scope for {service_type}")
            provider = self._scoped_factories[service_type]
            return scope.get_or_create(service_type, provider)  # type: ignore[return-value]

        if service_type in self._providers:
            provider = self._providers[service_type]
            return provider()

        raise ServiceNotRegisteredError(f"Service not registered: {service_type}")

    def create_scope(self) -> Scope:
        return ServiceScope(self)

    @contextmanager
    def scope_context(self) -> Generator[Scope, None, None]:
        scope = self.create_scope()
        old_scope = getattr(self._local, 'current_scope', None)
        self._local.current_scope = scope
        try:
            yield scope
        finally:
            scope.clear()
            self._local.current_scope = old_scope

    def _get_current_scope(self) -> Optional[ServiceScope]:
        return getattr(self._local, 'current_scope', None)

    def wire(self, modules: list[str]) -> None:
        self._container.wire(modules=modules)

    def is_registered(self, service_type: Type[Any]) -> bool:
        return (service_type in self._providers or
                service_type in self._scoped_factories)

    def get_registration_info(self, service_type: Type[Any]) -> Optional[str]:
        if service_type in self._providers:
            provider = self._providers[service_type]
            if isinstance(provider, providers.Singleton):
                return "singleton"
            elif isinstance(provider, providers.Factory):
                return "transient"
        elif service_type in self._scoped_factories:
            provider_factory = self._scoped_factories[service_type]
            if callable(provider_factory) and not isinstance(provider_factory, type):
                return "scoped (factory)"
            else:
                return "scoped (class)"
        return None

    def list_registered_services(self) -> Dict[str, list[str]]:
        return {
            "singletons": [str(t) for t in self._providers.keys()
                           if isinstance(self._providers[t],
                                         providers.Singleton)],
            "transients": [str(t) for t in self._providers.keys()
                           if isinstance(self._providers[t],
                                         providers.Factory)],
            "scoped": [str(t) for t in self._scoped_factories.keys()]
        }