# Problem 32: Pandigital products

## Problem

We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.

## Implementation


```python
# Solution
def pandigital_products(digits: set[int]) -> int:
    import itertools

    max_digits_left = int(len(digits)-1/2)

    def tuple_to_int(t: tuple[int]) -> int:
        return sum(d*10**i for i, d in enumerate(t))

    products = set()
    for num_digits_left in range(1, max_digits_left+1):
        for left_factor_digits in itertools.permutations(digits, r=num_digits_left):
            remaining_digits_after_left = digits - set(left_factor_digits)
            left_factor = tuple_to_int(left_factor_digits)
            for num_digits_right in range(1, min(num_digits_left, len(digits)-num_digits_left*2+1)):
                for right_factor_digits in itertools.permutations(remaining_digits_after_left, r=num_digits_right):
                    remaining_digits_after_right = remaining_digits_after_left - set(right_factor_digits)
                    right_factor = tuple_to_int(right_factor_digits)
                    prod = left_factor*right_factor
                    prod_str = str(prod)
                    if len(prod_str)!=len(remaining_digits_after_right):
                        continue
                    if all(str(d) in prod_str for d in remaining_digits_after_right):
                        products.add(prod)
                        print(f"{left_factor}*{right_factor} = {prod}")
    return sum(products)
# END solution

from IPython.display import  Markdown

DIGITS = set(range(1, 10))
solution = pandigital_products(digits=DIGITS)

Markdown(f"""
## Solution

Sum of pandigital products using digits 1 through 9: {solution}
""")
```

    483*12 = 5796
    186*39 = 7254
    157*28 = 4396
    297*18 = 5346
    138*42 = 5796
    198*27 = 5346
    159*48 = 7632
    1963*4 = 7852
    1738*4 = 6952






## Solution

Sum of pandigital products using digits 1 through 9: 45228



