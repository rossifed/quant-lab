from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from shared.di.protocols import DIContainer


class TransactionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, container: DIContainer):
        super().__init__(app)
        self.container = container

    async def dispatch(self, request: Request, call_next):
        # Créer un scope pour cette requête
        with self.container.scope_context():
            # Le scope est maintenant actif pour ce thread
            response = await call_next(request)
            return response