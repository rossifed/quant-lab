# backtesting/main.py

from fastapi import FastAPI # type: ignore
from shared.messaging.protocols import build_messaging_client
from shared.messaging.protocols import MessagingClient

app = FastAPI()
messaging_client: MessagingClient | None = None

@app.on_event("startup")
async def startup():
    global messaging_client
    messaging_client = await build_messaging_client()
    await messaging_client.start()

@app.on_event("shutdown")
async def shutdown():
    if messaging_client:
        await messaging_client.stop()
