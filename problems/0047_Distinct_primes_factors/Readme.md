# Problem 47: Distinct primes factors

## Problem

The first two consecutive numbers to have two distinct prime factors are:

$$ 14 = 2 \times 7 $$
$$ 15 = 3 \times 5 $$

The first three consecutive numbers to have three distinct prime factors are:

$$ 644 = 2^{2} \times 7 \times 23 $$
$$ 645 = 3 \times 5 \times 43 $$
$$ 646 = 2 \times 17 \times 19 $$

Find the first four consecutive integers to have four distinct prime factors each. What is the first of these numbers?


## Implementation


```python
# Solution
def distinct_prime_factors(n_factors: int = 4, search_limit: int = 1000000) -> int:
    from collections import defaultdict

    composites = defaultdict(lambda: 0)
    consecutive = 0
    for i in range(2, search_limit+1):
        if i not in composites:
            for j in range(i, search_limit+1, i):
                composites[j] += 1

        if composites[i] != n_factors:
            consecutive = 0
            continue

        consecutive += 1
        if consecutive == n_factors:
            return i - n_factors + 1
    raise Exception("Not found within limit")
# END solution


from IPython.display import  Markdown

solution = distinct_prime_factors()

Markdown(f"""
## Solution

First member of the smallest sequence of 4 numbers with 4 distinct factors: {solution}
""")
```





## Solution

First member of the smallest sequence of 4 numbers with 4 distinct factors: 134043



