from fastapi import APIRouter, Depends
from shared.di.fastapi_injector import inject
from optimization.services.optimization_service import OptimizationService

router = APIRouter()

@router.get("/hello")
def hello_endpoint(service: OptimizationService = Depends(inject(OptimizationService))):
    return {"message": service.hello_world()}