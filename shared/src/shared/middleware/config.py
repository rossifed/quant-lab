from shared.di.protocols import DIContainer
from fastapi import FastAPI
from shared.middleware.transaction_middleware import TransactionMiddleware


def register_middleware(app: FastAPI, container: DIContainer):
    app.add_middleware(TransactionMiddleware, container=container)