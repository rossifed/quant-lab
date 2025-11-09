# shared/messaging/implementation/kafka/messaging_client.py
from shared.messaging.protocols import MessagingClient, MessageBroker


class KafkaMessagingClient(MessagingClient):
    def __init__(self, broker: MessageBroker):
        self._broker = broker
        self._started = False

    async def start(self) -> None:
        self._started = True

    async def stop(self) -> None:
        self._started = False

    @property
    def broker(self) -> MessageBroker:
        return self._broker
