# Problem 20: Factorial digit sum

## Problem

$n!$ means $n × (n − 1) × ... × 3 × 2 × 1$

For example, $10! = 10 × 9 × ... × 3 × 2 × 1 = 3628800$,
and the sum of the digits in the number $10!$ is $3 + 6 + 2 + 8 + 8 + 0 + 0 = 27$.

Find the sum of the digits in the number $100!$


## Implementation


```python
# Solution
def sum_factorial_digits_with_math_lib(n: int) -> int:
    import math
    return sum(map(int, str(math.factorial(n))))

def sum_factorial_digits_without_math_lib(n: int) -> int:
    from functools import reduce
    return sum(map(int, str(reduce(lambda a,b: a*b, range(1, n+1), 1))))
# END Solution


from IPython.display import  Markdown

N = 100
# solution = sum_factorial_digits_with_math_lib(n=N)
solution = sum_factorial_digits_without_math_lib(n=N)

Markdown(f"""
## Solution

Sum of digits in number ${N}!$: {solution}
""")
```





## Solution

Sum of digits in number $100!$: 648



