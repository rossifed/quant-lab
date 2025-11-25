import time
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from services.optimization.application.services.optimization_service import OptimizationService
from shared.di.injection import inject

router = APIRouter()


class BenchmarkRequest(BaseModel):
    """Benchmark configuration."""
    sleep_seconds: float = Field(default=1.0, ge=0.1, le=10.0, description="Sleep duration per task (0.1-10 seconds)")
    iterations: int = Field(default=10, ge=1, le=200, description="Number of sum computations (1-200)")
    use_ray: bool = Field(default=True, description="Use Ray for parallel execution")


class BenchmarkResponse(BaseModel):
    """Benchmark results."""
    config: BenchmarkRequest
    total_time_seconds: float
    tasks_completed: int
    throughput_tasks_per_second: float
    avg_time_per_task_seconds: float


@router.get("/hello")
async def hello(service: OptimizationService = Depends(inject(OptimizationService))):
    message = await service.hello_world()
    return {"message": message}


@router.post("/benchmark", response_model=BenchmarkResponse)
async def benchmark(
    request: BenchmarkRequest,
    service: OptimizationService = Depends(inject(OptimizationService))
) -> BenchmarkResponse:
    """Benchmark optimization service with configurable parameters."""
    start_time = time.time()
    
    # Run benchmark
    await service.benchmark(
        iterations=request.iterations,
        sleep_seconds=request.sleep_seconds,
        use_ray=request.use_ray
    )
    
    total_time = time.time() - start_time
    
    return BenchmarkResponse(
        config=request,
        total_time_seconds=round(total_time, 2),
        tasks_completed=request.iterations,
        throughput_tasks_per_second=round(request.iterations / total_time, 2),
        avg_time_per_task_seconds=round(total_time / request.iterations, 2)
    )
