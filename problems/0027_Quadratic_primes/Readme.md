# Problem 27: Quadratic primes

## Problem

Euler discovered the remarkable quadratic formula:

$$n^2 + n + 41$$

It turns out that the formula will produce 40 primes for the consecutive integer values $0 <= n <= 39$. However, when $n = 40, 40^2+40+41 = 40(40+1) + 41$ is divisible by 41, and certainly when $n = 41, 41^2 + 41 + 41$ is clearly divisible by 41.

The incredible formula $n^2 + 79n + 1601$ was discovered, which produces 80 primes for the consecutive values $ 0 <= n <= 79$. The product of the coefficients, −79 and 1601, is −126479.

Considering quadratics of the form:

$n^2 + an + b$, where $|a|<1000$ and $|b|<1000$ and

where $|n|$ is the modulus/absolute value of $n$
e.g. $|11| = 11$ and $|-4| = 4$

Find the product of the coefficients, $a$ and $b$, for the quadratic expression that produces the maximum number of primes for consecutive values of $n$, starting with $n = 0$.

## Implementation


```python
def max_consecutive_primes_product(upper_limit: int) -> int:
    import itertools
    from functools import lru_cache
    from sympy import isprime


    @lru_cache(maxsize=5000)
    def grade_2_term(np: int):
        return np**2

    @lru_cache(maxsize=5000)
    def grade_1_term(ap: int, np: int):
        return ap*np

    @lru_cache(maxsize=5000)
    def is_prime(p: int):
        return isprime(p)


    max_consecutive_primes = (0, 0, 0)
    for a, b in itertools.product(range(-upper_limit+1, upper_limit), range(-upper_limit, upper_limit+1)):
        n = 0
        consecutive_primes = 0
        while is_prime(grade_2_term(n)+grade_1_term(a, n)+b):
            n += 1
            consecutive_primes += 1
            if consecutive_primes > max_consecutive_primes[0]:
                max_consecutive_primes = (consecutive_primes, a, b)
    consecutive_primes, sol_a, sol_b = max_consecutive_primes
    print(f"Max consecutive primes = {consecutive_primes} (a={sol_a}, b={sol_b})")
    return sol_a * sol_b
# END Solution


from IPython.display import  Markdown

UPPER_LIMIT = 1000
solution = max_consecutive_primes_product(upper_limit=UPPER_LIMIT)

Markdown(f"""
## Solution

Product $ab$ for $a, b$ that produce the maximum number of primes: {solution}
""")
```

    Max consecutive primes = 71 (a=-61, b=971)






## Solution

Product $ab$ for $a, b$ that produce the maximum number of primes: -59231



