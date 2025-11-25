from pydantic import BaseModel


class OptimizationDone(BaseModel):
    """Event: Optimization result (sum of two numbers)."""
    num1: int
    num2: int
    result: int
    
    def __str__(self) -> str:
        return f"OptimizationDone({self.num1} + {self.num2} = {self.result})"
    
    def to_dict(self) -> dict:
        return self.model_dump()
