from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def hello():
    return {"message": "Hello from backtesting service"}


@router.post("/backtest")
async def run_backtest():
    return {"status": "backtest started"}
