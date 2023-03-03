# Problem 48: Prime permutations

## Problem

The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330, is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property, but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?




## Implementation


```python
# Solution
def prime_permutations(n_digits: int = 4) -> int:
    import itertools
    import sympy

    matches = []

    for i_tuple in itertools.combinations_with_replacement("123456789", r=n_digits):
        prime_combinations = [
            n
            for n_tuple in set(itertools.permutations(i_tuple))
            if sympy.isprime((n := int(''.join(n_tuple))))
        ]

        if len(prime_combinations) < 3:
            continue

        for p_1 in prime_combinations:
            for p_2 in prime_combinations:
                if p_2 > p_1 and (p_3 := p_2 + (p_2 - p_1)) in prime_combinations:
                    matches.append(f"{p_1}{p_2}{p_3}")

    print(matches)
    return [match for match in matches if not match.startswith("1487")][0]
# END solution


from IPython.display import  Markdown

solution = prime_permutations()

Markdown(f"""
## Solution

12-digit number formed from concatenating 3 prime terms, permutations of themselves and separated for a common number: {solution}
""")
```

    ['148748178147', '296962999629']






## Solution

12-digit number formed from concatenating 3 prime terms, permutations of themselves and separated for a common number: 296962999629



