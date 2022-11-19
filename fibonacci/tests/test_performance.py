import pytest
from fibonacci.dynamic import fibonacci_dynamic_v2


@pytest.mark.performance
def test_performance():
    fibonacci_dynamic_v2(1000)
