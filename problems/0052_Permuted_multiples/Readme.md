# Problem 52: Permuted multiples

## Problem

It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.


## Implementation


```python
# Auxiliar
def multiples_have_same_digit(number: int, number_of_multiples: int):
    number_digits = list(sorted(int(digit) for digit in str(number)))
    i = 2
    while i <= number_of_multiples:
        if list(sorted(int(digit) for digit in str(number * i))) != number_digits:
            return False
        i+=1
    return True

# Solution
def permuted_multiples(number_of_multiples: int, starting_number: int = 1) -> int:
    i = starting_number
    while True:
        # if i % 1000 == 0:
        #     print(f"Checking number {i}...")
        if multiples_have_same_digit(i, number_of_multiples):
            return i
        i += 1
# END solution


from IPython.display import  Markdown

solution = permuted_multiples(6)

Markdown(f"""
## Solution
Smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits: {solution}
""")
```





## Solution
## Problem
Smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits: 142857



