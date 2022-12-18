# Problem 37: Truncatable primes

## Problem

The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right, and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.

## Implementation


```python
# Solution
def truncatable_primes() -> int:
    from sympy import isprime
    import itertools

    left_truncatables = {2, 3, 5, 7}
    right_truncatables = {2, 3, 5, 7}
    right_allowed_extensions = {1, 3, 7, 9}
    left_allowed_extensions = range(0, 10)
    complete_truncatables = set()
    while left_truncatables and right_truncatables:
        left_truncatables = set(p for p in [int(f"{e}{t}") for (e, t) in itertools.product(left_allowed_extensions, left_truncatables)] if isprime(p))
        right_truncatables = set(p for p in [int(f"{t}{e}") for (e, t) in itertools.product(right_allowed_extensions, right_truncatables)] if isprime(p))
        complete_truncatables.update(left_truncatables.intersection(right_truncatables))

    assert len(complete_truncatables) == 11
    # print(sorted(list(complete_truncatables)))
    return sum(complete_truncatables)
# END solution

from IPython.display import  Markdown

solution = truncatable_primes()

Markdown(f"""
## Solution

Sum of truncatable primes: {solution}
""")
```





## Solution

Sum of truncatable primes: 748317



