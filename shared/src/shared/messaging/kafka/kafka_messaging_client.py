from aiokafka import AIOKafkaProducer, AIOKafkaConsumer  # type: ignore


class KafkaMessagingClient:
    def __init__(self,
                 producer: AIOKafkaProducer, 
                 consumer: AIOKafkaConsumer):
        self._producer = producer
        self._consumer = consumer
          
    async def start(self):
        await self._producer.start()
        await self._consumer.start()

    async def stop(self):
        await self._producer.stop()
        await self._consumer.stop()