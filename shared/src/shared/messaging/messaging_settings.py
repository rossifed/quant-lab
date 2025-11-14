# shared/messaging/config.py
from typing import Protocol


class MessagingSettings(Protocol):
    def get_backend(self) -> str:
        ...
