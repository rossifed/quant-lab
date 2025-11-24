from fastapi import APIRouter, Depends
from services.optimization.application.services.optimization_service import OptimizationService
from shared.di.injection import inject

router = APIRouter()




@router.get("/hello")
async def hello(service: OptimizationService = Depends(inject(OptimizationService))):
    message = await service.hello_world()
    return {"message": message}
