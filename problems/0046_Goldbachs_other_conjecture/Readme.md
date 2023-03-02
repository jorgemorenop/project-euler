# Problem 46: Goldbach's other conjecture

## Problem

It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

$$9 = 7 + 2\times1^2$$
$$15 = 7 + 2\times2^2$$
$$21 = 3 + 2\times3^2$$
$$25 = 7 + 2\times3^2$$
$$27 = 19 + 2\times2^2$$
$$33 = 31 + 2\times1^2$$

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?

## Implementation


```python
# Solution
def goldbach_other_conjecture() -> int:
    import math
    import sympy

    primes = {2}
    i = 3
    while True:
        if sympy.isprime(i):
            primes.add(i)

        combination_found = False
        for prime in primes:
            if math.sqrt((i - prime) / 2).is_integer():
                combination_found = True
                break
        if not combination_found:
            return i

        # Update for next iteration
        i += 2
# END solution


from IPython.display import  Markdown

solution = goldbach_other_conjecture()

Markdown(f"""
## Solution

Smallest odd composite that cannot be written as the sum of a prime and twice a square: {solution}
""")
```





## Solution

Smallest odd composite that cannot be written as the sum of a prime and twice a square: 5777



