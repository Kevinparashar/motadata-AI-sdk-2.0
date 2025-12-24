"""
Concurrency utilities (asyncio, threading)
"""
import asyncio
from typing import Callable, Any, List, Coroutine
from concurrent.futures import ThreadPoolExecutor, Executor
from threading import Thread, Lock


class AsyncExecutor:
    """Async executor for running async functions"""
    
    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self.loop = None
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute a function asynchronously"""
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return await asyncio.get_event_loop().run_in_executor(
                self.executor, func, *args, **kwargs)
    
    def run(self, coro: Coroutine) -> Any:
        """Run a coroutine in the event loop"""
        if self.loop is None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        return self.loop.run_until_complete(coro)
    
    def shutdown(self):
        """Shutdown the executor"""
        if self.executor:
            self.executor.shutdown(wait=True)


class ThreadPool:
    """Thread pool for parallel execution"""
    
    def __init__(self, max_workers: int = 5):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def submit(self, func: Callable, *args, **kwargs):
        """Submit a task to the thread pool"""
        return self.executor.submit(func, *args, **kwargs)
    
    def map(self, func: Callable, iterable: List[Any]) -> List[Any]:
        """Map function over iterable in parallel"""
        return list(self.executor.map(func, iterable))
    
    def shutdown(self, wait: bool = True):
        """Shutdown the thread pool"""
        self.executor.shutdown(wait=wait)


class ThreadSafeCounter:
    """Thread-safe counter"""
    
    def __init__(self, initial_value: int = 0):
        self._value = initial_value
        self._lock = Lock()
    
    def increment(self, amount: int = 1) -> int:
        """Increment the counter"""
        with self._lock:
            self._value += amount
            return self._value
    
    def decrement(self, amount: int = 1) -> int:
        """Decrement the counter"""
        with self._lock:
            self._value -= amount
            return self._value
    
    @property
    def value(self) -> int:
        """Get the current value"""
        with self._lock:
            return self._value
