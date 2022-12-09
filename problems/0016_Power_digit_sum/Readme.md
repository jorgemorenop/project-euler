# Problem 16: Power digit sum

## Problem

$2^15 = 32768$ and the sum of its digits is $3 + 2 + 7 + 6 + 8 = 26$.

What is the sum of the digits of the number $2ˆ1000$?


## Implementation


```python
# Solution

def power_digit_sum(power: int) -> int:
    return sum(int(i) for i in str(2**power))

# END Solution

from IPython.display import  Markdown

POWER = 1000

Markdown(f"""
## Solution

Sum of the digits of $2^{{{POWER}}}$: {power_digit_sum(power=POWER)}
""")
```





## Solution

Sum of the digits of $2^{1000}$: 1366



