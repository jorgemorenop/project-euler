# Problem 23: Non-abundant sums

## Problem

A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number n is called deficient if the sum of its proper divisors is less than n and it is called abundant if this sum exceeds n.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.



## Implementation


```python
# Solution
def non_abundant_sums_bruteforce() -> int:
    import math

    upper_limit = 28123
    # upper_limit = 30000

    divisors: dict[int, set] = {1: {1}}
    abundant_numbers = []

    primes = []
    for i in range(2, upper_limit):
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

        if sum(divisors[i]) > i:
            abundant_numbers.append(i)

    abundant_sums = set(abundant_numbers[i]+abundant_numbers[j] for i in range(len(abundant_numbers)) for j in range(i, len(abundant_numbers)))
    non_abundant_sums = [i for i in range(1, upper_limit+1) if i not in abundant_sums]
    return sum(non_abundant_sums)
# END Solution


from IPython.display import  Markdown

solution = non_abundant_sums_bruteforce()

Markdown(f"""
## Solution

Sum of all possible integers that cannot be written as the sum of two abundant numbers: {solution}
""")
```





## Solution

Sum of all possible integers that cannot be written as the sum of two abundant numbers: 4179871



