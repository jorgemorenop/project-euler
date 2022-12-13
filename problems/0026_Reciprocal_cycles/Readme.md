# Problem 26: Reciprocal cycles

## Problem

A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:

1/2	= 	0.5
1/3	= 	0.(3)
1/4	= 	0.25
1/5	= 	0.2
1/6	= 	0.1(6)
1/7	= 	0.(142857)
1/8	= 	0.125
1/9	= 	0.(1)
1/10	= 	0.1

Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.

## Implementation


```python
def longest_reciprocal_cycle(upper_limit: int) -> int:
    from decimal import Decimal, getcontext
    from mpmath import mp

    max_check = upper_limit
    getcontext().prec = max_check * 2
    mp.dps = max_check * 2

    max_cycle_size = (0, 0)
    for d in range(1, upper_limit):
        n = Decimal(1)/Decimal(d)
        if len(str(n)) < max_check * 2:
            continue
        dec_str = str(n).strip('0.')
        cycle_size = -1
        begin_skip = 0
        while cycle_size == -1 and begin_skip < max_check / 2:
            for i in range(1, max_check - begin_skip):
                if dec_str[begin_skip:i] == dec_str[begin_skip+i:2*i]:
                    cycle_size = i
                    break
            begin_skip += 1
        # print(f"1/{d} (cycle size = {cycle_size})= {n}")
        if cycle_size > max_cycle_size[0]:
            max_cycle_size = (cycle_size, d)
    # print(f"Max cycle size: {max_cycle_size[0]} (d={max_cycle_size[1]}) ({Decimal(1)/Decimal(max_cycle_size[1])})")
    return max_cycle_size[1]
# END solution

from IPython.display import  Markdown

UPPER_LIMIT = 1_000
solution = longest_reciprocal_cycle(upper_limit=UPPER_LIMIT)

Markdown(f"""
## Solution

d for d<{UPPER_LIMIT} for which $1/d$ has the longest recurring cycle in its decimal fraction part: {solution}
""")
```





## Solution

d for d<1000 for which $1/d$ has the longest recurring cycle in its decimal fraction part: 983



