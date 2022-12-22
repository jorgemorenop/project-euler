# Problem 43: Sub-string divisibility

## Problem

The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.

Let d1 be the 1st digit, d2 be the 2nd digit, and so on. In this way, we note the following:

- $d_2d_3d_4=406$ is divisible by 2
- $d_3d_4d_5=063$ is divisible by 3
- $d_4d_5d_6=635$ is divisible by 5
- $d_5d_6d_7=357$ is divisible by 7
- $d_6d_7d_8=572$ is divisible by 11
- $d_7d_8d_9=728$ is divisible by 13
- $d_8d_9d_{10}=289$ is divisible by 17

Find the sum of all 0 to 9 pandigital numbers with this property.

## Implementation


```python
# Solution
def substring_divisibility() -> int:
    import itertools

    def matches_property(n_tuple: tuple[str]):
        primes = [2, 3, 5, 7, 11, 13, 17]
        return all([int(''.join(n_tuple[i:i+3])) % primes[i-1] == 0 for i in range(1, 8)])

    allowed_digits = ''.join(str(i) for i in range(0, 10))
    return sum(int(''.join(n)) for n in filter(matches_property, itertools.permutations(allowed_digits)))
# END solution


from IPython.display import  Markdown

solution = substring_divisibility()

Markdown(f"""
## Solution

Sum of pandigital numbers that match property: {solution}
""")
```





## Solution

Sum of pandigital numbers that match property: 16695334890



