from fastapi import APIRouter, Depends
from services.backtesting.application.services.backtesting_service import BacktestingService
from shared.di.injection import inject

router = APIRouter()


@router.get("/hello")
async def hello(service: BacktestingService = Depends(inject(BacktestingService))):
    message = await service.hello_world()
    return {"message": message}


@router.post("/backtest")
async def run_backtest(service: BacktestingService = Depends(inject(BacktestingService))):
    result = await service.run_backtest()
    return {"status": result}
