from shared.logging.protocols import Logger
from shared.messaging import MessageHandler
from services.optimization.application.integration_events.backtest_completed import BacktestCompletedReceived


class BacktestMessageHandler(MessageHandler):
    """Handler for backtest completion messages."""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    async def handle(self, message_data: dict) -> None:
        """Handle incoming backtest completed messages."""
        event = BacktestCompletedReceived(**message_data)
        self.logger.info(f"Received backtest event: {event}")
