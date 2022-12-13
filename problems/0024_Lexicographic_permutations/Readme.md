# Problem 24: Lexicographic permutations

## Problem

A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

012   021   102   120   201   210

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?



## Implementation


```python
# Solution
def lexicographic_permutations(n: int, max_digit: int) -> str:
    import math

    assert math.factorial(max_digit+1) > n, "number of possible permutations is lower than N"

    digits = list(range(max_digit+1))
    res = ""
    m = n - 1
    while digits:
        combinations = math.factorial(len(digits)-1)
        pos, m = divmod(m, combinations)
        res += str(digits.pop(pos))
    return res
# END Solution


from IPython.display import  Markdown

N = 1_000_000
MAX_DIGIT = 9
solution = lexicographic_permutations(n=N, max_digit=MAX_DIGIT)

Markdown(f"""
## Solution

{N}-th lexicographic permutation of {' '.join(str(i) for i in range(MAX_DIGIT+1))}: {solution}
""")
```





## Solution

1000000-th lexicographic permutation of 0 1 2 3 4 5 6 7 8 9: 2783915460



