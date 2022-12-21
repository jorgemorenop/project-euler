# Problem 41: Pandigital prime

## Problem

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.

What is the largest n-digit pandigital prime that exists?

## Implementation


```python
# Solution
def largest_pandigital_prime() -> int:
    import itertools
    from sympy import isprime

    # Skipping 9-digits (9+8+...+1 = 45, divisible by 3) and 8-digits (8+7+...+1 = 36, divisible by 3)
    for n in range(7, 0, -1):
        allowed_digits = ''.join(str(i) for i in range(n, 0, -1))
        for p_t in itertools.permutations(allowed_digits):
            p = int(''.join(p_t))
            if isprime(p):
                return p
    raise ArithmeticError("Pandigital prime not found")
# END solution


from IPython.display import  Markdown

solution = largest_pandigital_prime()

Markdown(f"""
## Solution

Largest pandigital prime  : {solution}
""")
```





## Solution

Largest pandigital prime  : 7652413



