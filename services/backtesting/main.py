from pathlib import Path
from fastapi import FastAPI
from shared import load_config, configure_services, create_lifespan, register_app_middleware
from services.backtesting.api.endpoints import router
from services.backtesting.registration import register_services


# Load configuration from YAML - no knowledge of messaging implementation!
config = load_config(Path(__file__).parent / "config.yaml")

# 1. Configure core services (logging, messaging)
container = configure_services(
    logging_settings=config.get_logging_settings(),
    messaging_settings=config.get_messaging_settings()
)

# 2. Register domain services
register_services(container)

# 3. Create FastAPI app with lifespan
app = FastAPI(title=config.app.name, lifespan=create_lifespan(container))  # type: ignore[arg-type]

# 4. Register middleware
register_app_middleware(app, container)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"service": config.app.name, "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
