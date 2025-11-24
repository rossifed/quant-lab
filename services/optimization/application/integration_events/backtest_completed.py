from dataclasses import dataclass
from datetime import datetime


@dataclass
class BacktestCompletedReceived:
    backtest_id: int
    result: str
    is_success: bool
    backtest_date: str
    
    def __str__(self) -> str:
        return f"BacktestCompletedReceived(id={self.backtest_id}, result={self.result}, success={self.is_success}, date={self.backtest_date})"