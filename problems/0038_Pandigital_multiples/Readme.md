# Problem 38: Pandigital multiples

## Problem

Take the number 192 and multiply it by each of 1, 2, and 3:

192 × 1 = 192

192 × 2 = 384

192 × 3 = 576


By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)

The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).

What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n > 1?

## Implementation


```python
# Solution
def pandigital_multiples() -> int:
    import itertools


    def is_pandigital_multiple(prod: int):
        prod_str = str(prod)
        for i in range(1, int(len(prod_str)/2) + 1):
            common_factor = int(prod_str[:i])
            number_tail = prod_str[i:]
            n = 2
            while number_tail and number_tail.startswith(str(n*common_factor)):
                number_tail = number_tail.lstrip(str(n*common_factor))
                n += 1
            if number_tail == '':
                return True
        return False

    for pan_number in reversed(sorted(int(''.join(p)) for p in itertools.permutations('123456789', 9))):
        if is_pandigital_multiple(pan_number):
            return pan_number

# END solution

from IPython.display import  Markdown

solution = pandigital_multiples()

Markdown(f"""
## Solution

Largest 9-digit number formed from concatenations of p*n (n = 1, 2, 3,...): {solution}
""")
```





## Solution

Largest 9-digit number formed from concatenations of p*n (n = 1, 2, 3,...): 932718654



