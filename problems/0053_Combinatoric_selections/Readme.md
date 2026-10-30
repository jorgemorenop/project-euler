# Problem 53: Permuted multiples

## Problem

There are exactly ten ways of selecting three from five, 12345:

$$123, 124, 125, 134, 135, 145, 234, 235, 245, 345$$

In combinatorics, we use the notation, $\binom{5}{3}=10$.

In general, $\binom{n}{r}=\frac{n!}{r!(n-r)!}$, where $r<=n$.

It is not until $n=23$, that a value exceeds one-million: $\binom{23}{10} = 1144066$.

How many, not necessarily distinct, values of $\binom{n}{r}$ for $1<=n<=100$, are greater than one-million?


## Implementation


```python
# Solution
import math

def permuted_multiples() -> int:
    """Solve the problem here.

    Line of thought:
        - as r increases, the distribution is a bell curve
        - if r=10 is the first value for n where (n over r) > one-million, then s=(n-r)=10, s>=r, is the last value where (n over s) is greater than one-million, and s-r+1 is the number of values greater than one-million for n
        - if (n over r) exceeds one-million, and m > n, then (m over r) already exceeds one-million
        - doesn't matter since we'll start in n=23 and r=10, but in case we wanted the algorithm to still work for other targets (besides 1M) or when starting on a lower number, we could start checking r values from n/2.
    :return:
    """
    factorial_cache = {}
    def get_factorial(p):
        if p not in factorial_cache:
            factorial_cache[p] = math.factorial(p)
        return factorial_cache[p]

    values_over_target = 0
    n = 23
    r = 10
    while n<=100:
        n_factorial = get_factorial(n)
        while r > 1:
            t = r-1 # Trying with next value of r
            if n_factorial / (get_factorial(t) * get_factorial(n-t)) > 1_000_000:
                r = t
            else:
                break
        values_over_target += (n-r)-r+1
        n+=1
    return values_over_target
# END solution


from IPython.display import  Markdown

solution = permuted_multiples()

Markdown(f"""
## Solution

How many values of (n over r) for 1<=n<=100 are greater than one-million?: {solution}
""")
```





## Solution

How many values of (n over r) for 1<=n<=100 are greater than one-million?: 4075





```python

```
