# shared/messaging/config.py

from pydantic import BaseSettings# type: ignore[misc]


class MessagingSettings(BaseSettings):
    backend: str = "kafka"
    bootstrap_servers: str = "redpanda:9092"

    class Config:
        env_prefix = "MESSAGING_"
        env_file = ".env"
