from shared.messaging import MessageHandler
from services.backtesting.application.integration_events.optimization_done import OptimizationDone
from services.backtesting.application.services.backtesting_service import BacktestingService


class OptimizationDoneHandler(MessageHandler):
    """Handler for optimization results - delegates to BacktestingService."""
    
    def __init__(self, backtesting_service: BacktestingService):
        self.backtesting_service = backtesting_service
    
    async def handle(self, message_data: dict) -> None:
        """Delegate to service for business logic."""
        event = OptimizationDone(**message_data)
        await self.backtesting_service.handle_optimization_result(
            event.num1, event.num2, event.result
        )
