from typing import List,Tuple,Callable,Dict
import pytest
from fibonacci.naive import fibonacci_naive


Decorator = Callable

def get_list_of_kwargs_for_function(
    identifiers:str, values: List[Tuple[str,str]]) -> List[Dict[str,str]]:
    print(f"getting list of kwargs for function,\n{identifiers=},{values=}")

def my_parametrized(identifiers: str, values: List[Tuple[int,int]]) -> Decorator:
    def my_parametrized_decorator(function:Callable) -> Callable:
        def run_func_parametrized() -> None:
            # parse arguments ("n,expected",[(0,0),(1,1),(2,1),(20,6765)])
            # run function multipe times with parse arguments
            list_of_kwargs_for_function = get_list_of_kwargs_for_function(
                identifiers=identifiers,values=values
            )
            for kwargs_for_function in list_of_kwargs_for_function:
                print(
                    f"calling function {function.__name__} with {kwargs_for_function}"
                )
                function(**kwargs_for_function)
        return my_parametrized_decorator

    return my_parametrized_decorator

# @pytest.mark.parametrize("n,expected",[(0,0),(1,1),(2,1),(20,6765)])
@my_parametrized(identifiers="n,expected",values=[(0,0),(1,1),(2,1),(20,6765)])
def test_naive(n:int,expected:int) -> None:
    res = fibonacci_naive(n=n)
    assert res == expected
