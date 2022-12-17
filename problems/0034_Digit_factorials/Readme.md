# Problem 34: Digit factorials

## Problem

145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: As 1! = 1 and 2! = 2 are not sums they are not included.

## Implementation


```python
# Solution
def digit_factorials() -> int:
    import math
    from functools import lru_cache

    @lru_cache(maxsize=10)
    def factorial(n: int):
        return math.factorial(n)

    upper_limit = factorial(9)*(int(math.log10(factorial(9)))+1)
    return sum(i for i in range(10, upper_limit) if sum(factorial(int(d)) for d in str(i)) == i)
# END solution

from IPython.display import  Markdown

solution = digit_factorials()

Markdown(f"""
## Solution

Sum of all numbers which are equal to the sum of the factorial of their digits: {solution}
""")
```





## Solution

Sum of all numbers which are equal to the sum of the factorial of their digits: 40730



