# Problem 21: Amicable numbers

## Problem

Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair and each of a and b are called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.


## Implementation


```python
# Solution
def sum_amicable_numbers(upper_limit: int):
    import math

    divisors: dict[int, set] = {1: {1}}
    sum_divisors: dict[int, int] = {1: 1}
    amicable_numbers = []

    primes = []
    for i in range(2, upper_limit+1):
        divisors[i] = {1}

        sqrt_i = math.sqrt(i)
        is_prime = True
        for p in primes:
            if p > sqrt_i:
                break
            if i % p == 0:
                divisors[i].update(divisors[int(i/p)].union({p * d for d in divisors[int(i/p)]}).union({int(i/p)}))
                is_prime = False
        if is_prime:
            primes.append(i)

        sum_divisors[i] = sum(divisors[i])
        if sum_divisors[i] < i and sum_divisors[sum_divisors[i]] == i:
            amicable_numbers.extend([i, sum_divisors[i]])

    # print(f"Amicable numbers: {amicable_numbers}")
    return sum(amicable_numbers)
# END Solution


from IPython.display import  Markdown

UPPER_LIMIT = 10000
solution = sum_amicable_numbers(upper_limit=UPPER_LIMIT)

Markdown(f"""
## Solution

Sum of amicable numbers below {UPPER_LIMIT}: {solution}
""")
```





## Solution

Sum of amicable numbers below 10000: 31626



