from dependency_injector.containers import DeclarativeContainer
from shared.di.adapter import DIContainerAdapter
from shared.di.protocols import DIContainer
from typing import Optional


class AppContainer(DeclarativeContainer):
    pass


def create_container() -> DIContainer:
    base_container = AppContainer()
    return DIContainerAdapter(base_container)


_container: Optional[DIContainer] = None


def get_container() -> DIContainer:
    global _container
    if _container is None:
        _container = create_container()
    return _container
