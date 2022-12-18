# Problem 36: Double-base palindromes

## Problem

The decimal number, 585 = 10010010012 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)

## Implementation


```python
# Solution
def double_base_palindromes(upper_limit: int) -> int:
    return sum(i for i in range(upper_limit) if str(i) == ''.join(reversed(str(i))) and f'{i:b}' == ''.join(reversed(f'{i:b}')))
# END solution

from IPython.display import  Markdown

UPPER_LIMIT = 1_000_000
solution = double_base_palindromes(upper_limit=UPPER_LIMIT)

Markdown(f"""
## Solution

Sum of numbers that are palindromic in base 10 and base 2: {solution}
""")
```





## Solution

Sum of numbers that are palindromic in base 10 and base 2: 872187



