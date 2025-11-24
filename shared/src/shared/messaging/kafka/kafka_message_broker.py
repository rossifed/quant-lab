import json
from aiokafka import AIOKafkaProducer  # type: ignore
from shared.messaging.protocols import Message, MessageBroker
from typing  import Iterable

class KafkaMessageBroker(MessageBroker):
    def __init__(self, producer: AIOKafkaProducer, default_topic: str = "events"):
        self._producer = producer
        self._default_topic = default_topic

    async def publish_async(self, message: Message) -> None:
        message_type = type(message).__name__
        
        if hasattr(message, 'to_dict'):
            message_data = message.to_dict()
        else:
            message_data = message.__dict__
        
        payload = json.dumps({
            "message_type": message_type,
            "data": message_data
        }).encode("utf-8")
        await self._producer.send_and_wait(self._default_topic, payload)

    async def publish_many_async(self, messages: Iterable[Message]) -> None:
        for message in messages:
            await self.publish_async(message)