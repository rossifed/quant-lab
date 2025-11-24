from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from shared.di.protocols import DIContainer
from typing import Callable, Awaitable


class ScopeMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, container: DIContainer) -> None:
        super().__init__(app)
        self.container = container

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        with self.container.scope_context():
            response = await call_next(request)
            return response