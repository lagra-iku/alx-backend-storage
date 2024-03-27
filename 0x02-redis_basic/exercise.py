#!/usr/bin/env python3
"""
a Python function that returns all students sorted by average score
"""

import functools
import uuid
import redis
from typing import Union, Callable


def call_history(method: Callable) -> Callable:
    """Decorator to store history of inputs and outputs for a function."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = method.__qualname__ + ":inputs"
        outputs_key = method.__qualname__ + ":outputs"

        # Store input arguments
        self._redis.rpush(inputs_key, str(args))

        # Execute the original function
        output = method(self, *args, **kwargs)

        # Store output
        self._redis.rpush(outputs_key, str(output))

        return output

    return wrapper


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def replay(method, redis_client: redis.Redis):
    """Display the history of calls for a particular function."""
    method_name = method.__qualname__
    inputs_key = method_name + ":inputs"
    outputs_key = method_name + ":outputs"

    inputs_history = redis_client.lrange(inputs_key, 0, -1)
    outputs_history = redis_client.lrange(outputs_key, 0, -1)

    print(f"{method_name} was called {len(inputs_history)} times:")

    for input_str, output_str in zip(inputs_history, outputs_history):
        input_args = eval(input_str.decode())
        output = output_str.decode()
        print(f"{method_name}(*{input_args}) -> {output}")


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Callable = None
    ) -> Union[str, bytes, int, None]:
        pass
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=int)
