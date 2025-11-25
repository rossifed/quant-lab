import asyncio
import time
from typing import Protocol
import ray
from shared.logging.protocols import Logger
from shared.messaging.protocols import MessageBroker
from services.optimization.application.integration_events.optimization_done import OptimizationDone


class OptimizationService(Protocol):
    async def compute_sum(self, num1: int, num2: int, sleep_seconds: float = 1.0) -> None:
        """Compute sum of two numbers and publish result."""
        ...
    
    async def benchmark(self, iterations: int, sleep_seconds: float, use_ray: bool) -> None:
        """Run benchmark with configurable parameters."""
        ...
    
    async def hello_world(self) -> str:
        ...


class RayOptimizationService(OptimizationService):
    """Ray-powered optimization service with parallel computation."""
    
    # Ray remote function as static method - pas besoin de self
    @staticmethod
    @ray.remote
    def _compute_sum_task(num1: int, num2: int, sleep_seconds: float = 1.0) -> tuple[int, int, int]:
        """CPU-intensive portfolio optimization."""
        # Simulate intensive portfolio optimization
        time.sleep(sleep_seconds)  # Simule calcul d'optimisation de portefeuille
        result = num1 + num2
        return num1, num2, result
    
    def __init__(self, message_broker: MessageBroker, logger: Logger):
        self.message_broker = message_broker
        self.logger = logger

    async def compute_sum(self, num1: int, num2: int, sleep_seconds: float = 1.0) -> None:
        """Compute portfolio optimization with Ray parallel execution."""
        self.logger.info(f"🔢 Submitting portfolio optimization to Ray: {num1} + {num2}...")
        
        # Submit task to Ray for parallel execution
        # Ray distribue automatiquement sur les workers disponibles
        future = self._compute_sum_task.remote(num1, num2, sleep_seconds)
        
        # Await result (non-blocking - Ray executes in parallel)
        # Pendant que ce calcul s'exécute, d'autres messages peuvent être traités
        num1_result, num2_result, result = await asyncio.to_thread(ray.get, future)
        
        self.logger.info(f"✅ Portfolio optimization complete: {num1_result} + {num2_result} = {result}")
        
        # Publish result
        result_event = OptimizationDone(num1=num1_result, num2=num2_result, result=result)
        await self.message_broker.publish_async(result_event)
    
    async def benchmark(self, iterations: int, sleep_seconds: float, use_ray: bool) -> None:
        """Run benchmark with Ray parallel execution."""
        self.logger.info(f"🏁 Starting Ray benchmark: {iterations} iterations, {sleep_seconds}s sleep")
        
        # Submit all tasks to Ray at once for parallel execution
        futures = [
            self._compute_sum_task.remote(i, i + 1, sleep_seconds)
            for i in range(iterations)
        ]
        
        # Wait for all results
        results = await asyncio.to_thread(ray.get, futures)
        
        self.logger.info(f"✅ Ray benchmark complete: {len(results)} tasks finished")
    
    async def hello_world(self) -> str:
        self.logger.info("Test Logger.Hello World Requested. ")
        return "Hello World from RayOptimizationService!"


# Keep old implementation for comparison
class DummyOptimizationService(OptimizationService):
    def __init__(self, message_broker: MessageBroker, logger: Logger):
        self.message_broker = message_broker
        self.logger = logger

    async def compute_sum(self, num1: int, num2: int, sleep_seconds: float = 1.0) -> None:
        """Compute sum with intensive calculation."""
        self.logger.info(f"🔢 Computing: {num1} + {num2}...")
        
        # Simulate intensive computation
        await asyncio.sleep(sleep_seconds)
        
        result = num1 + num2
        
        self.logger.info(f"✅ Result: {num1} + {num2} = {result}")
        
        # Publish result
        result_event = OptimizationDone(num1=num1, num2=num2, result=result)
        await self.message_broker.publish_async(result_event)
    
    async def benchmark(self, iterations: int, sleep_seconds: float, use_ray: bool) -> None:
        """Run benchmark without Ray (sequential asyncio)."""
        self.logger.info(f"🏁 Starting sequential benchmark: {iterations} iterations, {sleep_seconds}s sleep")
        
        # Run all tasks concurrently with asyncio (not Ray)
        tasks = [
            self._compute_task(i, i + 1, sleep_seconds)
            for i in range(iterations)
        ]
        
        await asyncio.gather(*tasks)
        
        self.logger.info(f"✅ Sequential benchmark complete: {iterations} tasks finished")
    
    async def _compute_task(self, num1: int, num2: int, sleep_seconds: float) -> tuple[int, int, int]:
        """Single computation task."""
        await asyncio.sleep(sleep_seconds)
        return num1, num2, num1 + num2
    
    async def hello_world(self) -> str:
        self.logger.info("Test Logger.Hello World Requested. ")
        return "Hello World from OptimizationService!"