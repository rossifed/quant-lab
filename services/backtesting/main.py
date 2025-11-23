from contextlib import asynccontextmanager
from fastapi import FastAPI
from shared import configure_services
from shared.messaging.kafka import KafkaMessagingClient
from services.backtesting.settings import Settings
from services.backtesting.api.endpoints import router


settings = Settings()

# Create app first
app = FastAPI(title=settings.app_name)

# Configure services (including middleware) before lifespan
container = configure_services(
    app=app,
    logging_settings=settings.get_logging_settings(),
    messaging_settings=settings.get_kafka_settings()
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - get container and start messaging
    messaging_client = container.resolve(KafkaMessagingClient)
    await messaging_client.start()
    
    yield
    
    # Shutdown
    await messaging_client.stop()


# Set lifespan after configuration
app.router.lifespan_context = lifespan

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"service": settings.app_name, "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
    return {"status": "healthy"}
