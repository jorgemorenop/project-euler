# Problem 17: Number letter counts

## Problem

If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?


**NOTE**: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.



## Implementation


```python
# Solution

def count_letters_of_numbers(lower_limit: int, upper_limit: int, verbose: bool = False) -> int:
    unit_to_string = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
             'seventeen', 'eighteen', 'nineteen']
    ten_to_string = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

    def number_to_string(number: int):
        assert number < 1_000_000, "Only numbers lower than 1 million are supported"

        thousands = int(number / 1000)
        thousand_str = '' if thousands == 0 else f'{number_to_string(thousands)} thousand'

        hundreds = int((number % 1000) / 100)
        hundred_str = '' if hundreds == 0 else f'{number_to_string(hundreds)} hundred'

        tens = int((number % 100)/10)
        units = number % 10
        ten_str = ten_to_string[tens]
        unit_str = teens[units] if tens == 1 else unit_to_string[units]

        ten_unit_join_str = '-' if ten_str and unit_str else ''
        hundred_ten_join = ' and ' if hundred_str and (ten_str or unit_str) else ''
        thousand_hundred_join = ' ' if thousand_str and hundred_str else ''
        return f'{thousand_str}{thousand_hundred_join}{hundred_str}{hundred_ten_join}{ten_str}{ten_unit_join_str}' \
               f'{unit_str}'

    def count_number_string(number_str: str):
        return len(number_str.replace(' ', '').replace('-', ''))

    total_count = 0
    for i in range(lower_limit, upper_limit+1):
        i_str = number_to_string(i)
        i_str_len = count_number_string(i_str)
        if verbose:
            print(f"{i}: {i_str} ({i_str_len} letters)")
        total_count += i_str_len
    return total_count

# END Solution


from IPython.display import  Markdown

LOWER_LIMIT = 1
UPPER_LIMIT = 1000

Markdown(f"""
## Solution

The count of letters of all numbers from {LOWER_LIMIT} to {UPPER_LIMIT} is: {count_letters_of_numbers(lower_limit=LOWER_LIMIT, upper_limit=UPPER_LIMIT)}
""")
```





## Solution

The count of letters of all numbers from 1 to 1000 is: 21124



