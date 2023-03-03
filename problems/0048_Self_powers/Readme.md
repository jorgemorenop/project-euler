# Problem 48: Self powers

## Problem



The series $1^1 + 2^2 + 3^3 + ... + 10^{10} = 10405071317$.

Find the last ten digits of the series, $1^1 + 2^2 + 3^3 + ... + 1000^{1000}$.



## Implementation


```python
# Solution
def self_powers(upper_limit: int = 1000) -> int:
    mod_factor = 10**10
    return sum((i**i) % mod_factor for i in range(1, upper_limit + 1)) % mod_factor
# END solution


from IPython.display import  Markdown

UPPER_LIMIT = 1000
solution = self_powers(upper_limit=UPPER_LIMIT)

Markdown(f"""
## Solution

Last 10 digits of $1^1 + 2^2 + 3^3 + ... + {UPPER_LIMIT}^{{{UPPER_LIMIT}}}$: {solution:010d}
""")
```





## Solution

Last 10 digits of $1^1 + 2^2 + 3^3 + ... + 1000^{1000}$: 9110846700



