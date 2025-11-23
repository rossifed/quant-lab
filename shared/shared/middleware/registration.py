from fastapi import FastAPI
from shared.di.protocols import DIContainer
from shared.middleware.scope_middleware import ScopeMiddleware


def add_middleware(app: FastAPI, container: DIContainer) -> None:
    app.add_middleware(ScopeMiddleware, container=container)
