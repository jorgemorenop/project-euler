# Problem 40: Champernowne's constant

## Problem

<p>An irrational decimal fraction is created by concatenating the positive integers:</p>
<p class="center">0.12345678910<span class="red strong">1</span>112131415161718192021...</p>
<p>It can be seen that the 12<sup>th</sup> digit of the fractional part is 1.</p>
<p>If <i>d</i><sub><i>n</i></sub> represents the <i>n</i><sup>th</sup> digit of the fractional part, find the value of the following expression.</p>
<p class="center"><i>d</i><sub>1</sub> × <i>d</i><sub>10</sub> × <i>d</i><sub>100</sub> × <i>d</i><sub>1000</sub> × <i>d</i><sub>10000</sub> × <i>d</i><sub>100000</sub> × <i>d</i><sub>1000000</sub></p>

## Implementation


```python
# Solution
def champernownes_constant() -> int:
    import math

    ns = [10 ** i for i in range(7)]
    dns = []
    for n in ns:
        digits_per_number = 0
        current_pos = prev_pos = 0
        while current_pos <= n:
            digits_per_number += 1
            new_digits = digits_per_number * (10**digits_per_number - 10**(digits_per_number-1))
            prev_pos = current_pos
            current_pos += new_digits
        q, r = divmod(n - prev_pos-1, digits_per_number)
        dns.append(int(str(10**(digits_per_number-1)+q)[r]))
        print(f"d{n} = {dns[-1]}")
    return math.prod(dns)


def champernownes_constant_bruteforce() -> int:
    import math

    ns = [10 ** i for i in range(7)]
    digits_str = ""
    digits_per_number = 0
    while len(digits_str) <= max(ns):
        digits_per_number += 1
        digits_str += "".join(str(i) for i in range(10**(digits_per_number-1), 10**digits_per_number))

    for n in ns:
        print(f"d{n} = {digits_str[n-1]}")

    return math.prod(int(digits_str[n-1]) for n in ns)

# END solution


from IPython.display import  Markdown

solution = champernownes_constant()
# solution = champernownes_constant_bruteforce()

Markdown(f"""
## Solution

Product of $d_{{1}} \\times d_{{10}} \\times d_{{100}} \\times d_{{1000}} \\times d_{{10000}} \\times d_{{100000}} \\times d_{{1000000}}$  : {solution}
""")
```

    d1 = 1
    d10 = 1
    d100 = 5
    d1000 = 3
    d10000 = 7
    d100000 = 2
    d1000000 = 1






## Solution

Product of $d_{1} \times d_{10} \times d_{100} \times d_{1000} \times d_{10000} \times d_{100000} \times d_{1000000}$  : 210



