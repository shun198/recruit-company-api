import pytest
from typing import Callable
from fibonacci.naive import fibonacci_naive
from fibonacci.cached import fibonacci_cached, fibonacci_lru_cached
from fixtures import time_tracker


@pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
@pytest.mark.parametrize("fib_func", [fibonacci_naive, fibonacci_cached, fibonacci_lru_cached])
def test_fibonacci(time_tracker,fib_func: Callable[[int], int], n: int, expected: int) -> None:
    res = fib_func(n)
    assert res == expected
