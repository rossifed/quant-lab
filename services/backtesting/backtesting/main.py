# services/backtesting/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from config import Settings
from shared.messaging.protocols import MessagingClient

settings = Settings()
messaging_client: MessagingClient | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global messaging_client

    # STARTUP
    messaging_client = await settings.init_messaging_client()

    yield  # ⬅️ App runs while inside this block

    # SHUTDOWN
    if messaging_client:
        await messaging_client.stop()

# 👇 This replaces on_event
app = FastAPI(lifespan=lifespan)
