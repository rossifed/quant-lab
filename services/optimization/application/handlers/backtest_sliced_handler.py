from shared.messaging import MessageHandler
from services.optimization.application.integration_events.backtest_sliced import BacktestSliced
from services.optimization.application.services.optimization_service import OptimizationService


class BacktestSlicedHandler(MessageHandler):
    """Handler for backtest slices - delegates to OptimizationService."""
    
    def __init__(self, optimization_service: OptimizationService):
        self.optimization_service = optimization_service
    
    async def handle(self, message_data: dict) -> None:
        """Delegate to service for business logic."""
        event = BacktestSliced(**message_data)
        await self.optimization_service.compute_sum(event.num1, event.num2)
