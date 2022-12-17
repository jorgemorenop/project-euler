# Problem 33: Digit cancelling fractions

## Problem

The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the denominator.

## Implementation


```python
# Solution
def digit_cancelling_fractions(num_digits: int) -> int:
    from fractions import Fraction
    import itertools

    min_number = 10**(num_digits-1)

    def remove_char(s: str, index: int):
        return s[:index]+s[index+1:]

    fractions_product = Fraction(1, 1)
    for denominator in range(min_number, 10**num_digits):
        for numerator in range(min_number, denominator):
            fraction = Fraction(numerator, denominator)
            numerator_str, denominator_str = str(numerator), str(denominator)
            can_simplify = any(den != 0 and fraction == Fraction(num, den) for num, den in [
                (int(remove_char(numerator_str, c1)), int(remove_char(denominator_str, c2)))
                for c1, c2 in itertools.product(range(len(numerator_str)), range(len(denominator_str)))
                if numerator_str[c1] == denominator_str[c2] != '0'
            ])
            if can_simplify:
                print(f"Can simplify fraction: {numerator}/{denominator}")
                fractions_product *= fraction

    return fractions_product.denominator
# END solution

from IPython.display import  Markdown

solution = digit_cancelling_fractions(num_digits=2)

Markdown(f"""
## Solution

Value of denominator of the product of the four fractions in their lowest terms: {solution}
""")
```

    Can simplify fraction: 16/64
    Can simplify fraction: 26/65
    Can simplify fraction: 19/95
    Can simplify fraction: 49/98






## Solution

Value of denominator of the product of the four fractions in their lowest terms: 100



