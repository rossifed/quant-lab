from typing import Protocol
from shared.logging.protocols import Logger
from shared.messaging.protocols import MessageBroker

class OptimizationService(Protocol):
    async def optimize(self) -> str:
        ...
    
    async def hello_world(self) -> str:
        ...

class DummyOptimizationService(OptimizationService):
    def __init__(self, message_broker: MessageBroker, logger: Logger):
        self.message_broker = message_broker
        self.logger = logger

    async def optimize(self) -> str:
        
        return "hello World"
    
    async def hello_world(self) -> str:
        self.logger.info("Test Logger.Hello World Requested. ")
        return "Hello World from OptimizationService!"