from fastapi import FastAPI
from shared import configure_services, create_lifespan, register_app_middleware
from services.optimization.settings import Settings
from services.optimization.api.endpoints import router
from services.optimization.registration import register_services


settings = Settings()

# 1. Configure core services (logging, messaging)
container = configure_services(
    logging_settings=settings.get_logging_settings(),
    messaging_settings=settings.get_kafka_settings()
)

# 2. Register domain services
register_services(container)

# 3. Create FastAPI app with lifespan (no knowledge of concrete messaging implementation)
app = FastAPI(title=settings.app_name, lifespan=create_lifespan(container))  # type: ignore[arg-type]

# 4. Register middleware
register_app_middleware(app, container)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"service": settings.app_name, "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}