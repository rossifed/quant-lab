"""Ray cluster connection manager for centralized initialization."""
import os
from typing import TYPE_CHECKING, Optional
import ray

if TYPE_CHECKING:
    from shared.logging.protocols import Logger


def initialize_ray_cluster(logger: Optional["Logger"] = None) -> None:
    """
    Initialize Ray cluster connection at application startup.
    
    This should be called once during app initialization, typically in main.py.
    Ray is a process-global singleton, so this establishes the connection
    that all services will use.
    
    Args:
        logger: Optional logger for connection status messages
        
    Environment Variables:
        RAY_ADDRESS: Ray cluster address (default: ray://ray-head:10001)
    """
    if ray.is_initialized():
        if logger:
            logger.info("⚡ Ray already initialized")
        return
    
    ray_address = os.getenv("RAY_ADDRESS", "ray://ray-head:10001")
    
    if logger:
        logger.info(f"🔌 Connecting to Ray cluster at {ray_address}...")
    
    ray.init(address=ray_address, ignore_reinit_error=True)
    
    if logger:
        logger.info(f"⚡ Ray cluster connected: {ray_address}")


def shutdown_ray_cluster(logger: Optional["Logger"] = None) -> None:
    """
    Shutdown Ray cluster connection at application shutdown.
    
    This should be called during app cleanup, typically in lifespan shutdown.
    
    Args:
        logger: Optional logger for shutdown status messages
    """
    if not ray.is_initialized():
        return
    
    if logger:
        logger.info("🔌 Shutting down Ray cluster connection...")
    
    ray.shutdown()
    
    if logger:
        logger.info("✅ Ray cluster disconnected")
