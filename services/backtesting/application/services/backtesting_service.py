from typing import Protocol
from shared.logging.protocols import Logger
from shared.messaging.protocols import MessageBroker
from services.backtesting.application.integration_events.backtest_sliced import BacktestSliced


class BacktestingService(Protocol):
    async def run_backtest(self) -> str:
        ...
    
    async def handle_optimization_result(self, num1: int, num2: int, result: int) -> None:
        """Handle optimization result."""
        ...
    
    async def hello_world(self) -> str:
        ...


class DummyBacktestingService(BacktestingService):
    def __init__(self, message_broker: MessageBroker, logger: Logger):
        self.message_broker = message_broker
        self.logger = logger

    async def run_backtest(self) -> str:
        """Generate numbers 1-10, slice into pairs, send each slice."""
        self.logger.info("🚀 Starting backtest - generating slices...")
        
        numbers = list(range(1, 101))  # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # Slice into pairs: (1,2), (3,4), (5,6), (7,8), (9,10)
        for i in range(0, len(numbers), 2):
            if i + 1 < len(numbers):
                slice_event = BacktestSliced(num1=numbers[i], num2=numbers[i + 1])
                
                self.logger.info(f"📤 Sending slice: ({slice_event.num1}, {slice_event.num2})")
                
                await self.message_broker.publish_async(slice_event)
        
        return "Backtest slices sent"
    
    async def handle_optimization_result(self, num1: int, num2: int, result: int) -> None:
        """Log the optimization result."""
        self.logger.info(f"✅ Optimization result: {num1} + {num2} = {result}")
    
    async def hello_world(self) -> str:
        return "Hello World from BacktestingService!"
