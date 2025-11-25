import json
from aiokafka import AIOKafkaProducer  # type: ignore
from shared.messaging.protocols import MessagePublisher


class KafkaMessagePublisher(MessagePublisher):
    """Kafka implementation of MessagePublisher."""
    
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer
    
    async def publish(self, channel: str, message: dict, message_type: str) -> None:
        """Publish a message to a Kafka topic.
        
        Args:
            channel: The Kafka topic to publish to
            message: The message payload as a dictionary
            message_type: The type of message being published
        """
        envelope = {
            "message_type": message_type,
            "data": message
        }
        
        payload = json.dumps(envelope).encode("utf-8")
        await self._producer.send(channel, payload)
