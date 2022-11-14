cache = {}

def fibonacci_cached(n:int) -> int:
    if n in cache:
        return cache[n]

    if n == 0 or n == 1:
        return n
