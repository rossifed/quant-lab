from pydantic import BaseModel


class BacktestSliced(BaseModel):
    """Event: Slice of numbers to optimize."""
    num1: int
    num2: int
    
    def __str__(self) -> str:
        return f"BacktestSliced(num1={self.num1}, num2={self.num2})"
    
    def to_dict(self) -> dict:
        return self.model_dump()
