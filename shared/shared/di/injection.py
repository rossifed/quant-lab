from typing import Type, Callable
from shared.di.container import get_container
from shared.di.protocols import T


def inject(cls: Type[T]) -> Callable[[], T]:
    def dependency() -> T:
        container = get_container()
        return container.resolve(cls)
    return dependency