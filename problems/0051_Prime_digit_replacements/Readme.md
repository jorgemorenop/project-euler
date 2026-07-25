# Problem 51: Prime digit replacements

## Problem


By replacing the 1st digit of the 2-digit number *3, it turns out that six of the nine possible values: 13, 23, 43, 53, 73, and 83, are all prime.

By replacing the 3rd and 4th digits of 56**3 with the same digit, this 5-digit number is the first example having seven primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993. Consequently 56003, being the first member of this family, is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family.



## Implementation


```python
import math
from itertools import product
# Auxiliary
def generate_primes(upper_limit: int, previous_primes: list[int] | None = None) -> list[int]:
    primes = [2, 3, 5] if not previous_primes else previous_primes
    i = max(list(primes))

    while i + 2 <= upper_limit:
        i += 2

        # if i % 5 == 0 or sum(int(d) for d in str(i)) % 3 == 0:
        #     continue

        is_prime = True
        sqrt_i = math.sqrt(i)
        for p in primes:
            if p > sqrt_i:
                break
            if i % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)


    return primes


def count_pattern_primes(pattern: str, primes: list[int]):
    """

    :param pattern: A pattern for the numbers, where * should be replaced by the same number (e.g.: 54**3 -> 54113 or 54223)
    :param primes:
    :return:
    """
    first_pattern_digit = 1 if pattern.startswith("*") else 0

    return sum([int(pattern.replace('*', str(i))) in primes for i in range(first_pattern_digit, 10)])


def create_patterns_for_number(number: int) -> set[str]:
    number_str = str(number)
    n_digits = len(number_str)
    map_combinations = [comb for comb in product(range(2), repeat=n_digits-1) if sum(comb)>0]  # Do not replace the last one! (not worth it)
    patterns = set()
    for combination in map_combinations:

        pattern = ""
        for i, digit in enumerate(combination):
            pattern += number_str[i] if not digit else "*"
        pattern += number_str[-1]
        patterns.add(pattern)
    return patterns


# Solution
def prime_digit_replacements(target_family_size: int, skip_first: int = 0, min_number_of_digits: int = 2) -> int:
    """ TODO.

    Things to take into account:
    - Numbers finishing in 0,2,4,5,6,8 can be skipped.
    -


    :return:
    """
    number_of_digits = min_number_of_digits
    primes = []
    tried_patterns = set()
    while True:
        n_digits_lower_limit = 10 ** (number_of_digits-1)
        n_digits_upper_limit = (10 ** number_of_digits) - 1
        primes = generate_primes(upper_limit=n_digits_upper_limit, previous_primes=primes)
        primes_with_n_digits = [prime for prime in primes if n_digits_lower_limit <= prime <= n_digits_upper_limit]
        for prime in primes_with_n_digits:
            if prime < skip_first:
                continue
            number_patterns = create_patterns_for_number(prime)
            for number_pattern in number_patterns:
                if number_pattern in tried_patterns:
                    continue
                # print(f"Trying pattern {number_pattern}")
                tried_patterns.add(number_pattern)
                pattern_count = count_pattern_primes(number_pattern, primes)
                if pattern_count >= target_family_size:
                    smallest_prime = number_pattern.replace("*", "1") if number_pattern.startswith("*") else number_pattern.replace("*", "0")
                    print(f"Found number family with {pattern_count} primes: {number_pattern}. Smallest prime in family: {smallest_prime}")
                    return smallest_prime
        number_of_digits+=1
# END solution


from IPython.display import  Markdown

solution = prime_digit_replacements(target_family_size=8)

Markdown(f"""
## Solution

Smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family: {solution}
""")
```

    Found number family with 8 primes: *2*3*3. Smallest prime in family: 121313






## Solution

Smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit, is part of an eight prime value family: 121313



