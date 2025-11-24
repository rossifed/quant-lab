from typing import Protocol
from datetime import datetime
from shared.logging.protocols import Logger
from shared.messaging.protocols import MessageBroker
from services.backtesting.application.events import BacktestCompletedEvent

class BacktestingService(Protocol):
    async def run_backtest(self) -> str:
        ...
    
    async def hello_world(self) -> str:
        ...

class DummyBacktestingService(BacktestingService):
    def __init__(self, message_broker: MessageBroker, logger: Logger):
        self.message_broker = message_broker
        self.logger = logger
        self._backtest_counter = 0

    async def run_backtest(self) -> str:
        self._backtest_counter += 1
        
        event = BacktestCompletedEvent(
            backtest_id=self._backtest_counter,
            result="Backtest completed successfully",
            is_success=True,
            backtest_date=datetime.now()
        )
        
        await self.message_broker.publish_async(event)
        
        self.logger.info(f"Published event: {event}")
        
        return event.result
    
    async def hello_world(self) -> str:
        return "Hello World from BacktestingService!"
