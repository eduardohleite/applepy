from typing import Optional, Callable, Any


def try_call(fn: Optional[Callable]) -> Any:
    if fn and callable(fn):
        return fn()
