from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class BacktestCompletedEvent:
    backtest_id: int
    result: str
    is_success: bool
    backtest_date: datetime
    
    def to_dict(self) -> dict:
        data = asdict(self)
        data['backtest_date'] = self.backtest_date.isoformat()
        return data
    
    def __str__(self) -> str:
        return f"BacktestCompletedEvent(id={self.backtest_id}, result={self.result}, success={self.is_success}, date={self.backtest_date})"
