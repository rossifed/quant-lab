from typing import (Protocol,
                    TypeVar,
                    Type,
                    Callable,
                    runtime_checkable,
                    Union)
from contextlib import AbstractContextManager

T = TypeVar("T")


class ServiceNotRegisteredError(Exception):
    pass


class Scope(Protocol):
    def get_or_create(self, service_type: Type[T], factory: Callable[[], T]) -> T: ...
    def clear(self) -> None: ...


@runtime_checkable
class DIContainer(Protocol):
    def add_singleton(self, service_type: Type[T],
                      provider: Union[Callable[[], T], T]) -> None: ...

    def add_transient(self, service_type: Type[T],
                      provider: Callable[[], T]) -> None: ...

    def add_scoped(self, service_type: Type[T],
                   provider: Callable[[], T]) -> None: ...

    def resolve(self, service_type: Type[T]) -> T: ...

    def wire(self, modules: list[str]) -> None: ...

    def scope_context(self) -> AbstractContextManager[Scope]: ...