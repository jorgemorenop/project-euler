# Problem 35: Circular primes

## Problem

The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?

## Implementation


```python
# Solution
def circular_primes(upper_limit: int) -> int:
    import math

    primes = [2]
    circular_primes_list = {2, 5}
    for i in range(3, upper_limit):
        is_prime = True
        sqrt_i = math.sqrt(i)
        for p in primes:
            if p > sqrt_i:
                break
            if i % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
            i_str = str(i)
            if all(d in ['1', '3', '7', '9'] for d in i_str):
                rotations = [int(i_str[i:] + i_str[:i]) for i in range(len(i_str))]
                if i == max(rotations) and all([r in primes for r in rotations[1:]]):
                    # print(f"More circular primes: {rotations}")
                    circular_primes_list.update(rotations)
        i += 2
    # print(f"Circular primes: {sorted(list(circular_primes_list))}")
    return len(circular_primes_list)
# END solution

from IPython.display import  Markdown

UPPER_LIMIT = 1_000_000
solution = circular_primes(upper_limit=UPPER_LIMIT)

Markdown(f"""
## Solution

Num of circular primes: {solution}
""")
```





## Solution

Num of circular primes: 55



