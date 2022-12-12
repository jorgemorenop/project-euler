# Problem 25: 1000-digit Fibonacci number

## Problem

The Fibonacci sequence is defined by the recurrence relation:

$F_n = F_{n−1} + F_{n−2}$, where $F_1 = 1$ and $F_2 = 1$

Hence the first 12 terms will be:

$$F_1 = 1$$
$$F_2 = 1$$
$$F_3 = 2$$
$$F_4 = 3$$
$$F_5 = 5$$
$$F_6 = 8$$
$$F_7 = 13$$
$$F_8 = 21$$
$$F_9 = 34$$
$$F_{10} = 55$$
$$F_{11} = 89$$
$$F_{12} = 144$$


The 12th term, $F_{12}$, is the first term to contain three digits.

What is the index of the first term in the Fibonacci sequence to contain 1000 digits?

## Implementation

Since the Fibonacci sequence converges to

$$\frac{{\phi}^n}{\sqrt(5)}$$

Where $\phi$ is the golden ratio.

Since the first digit with 1000 digits is $10^{999}$, if we want to get the first whole number such that

$$\frac{{\phi}^n}{\sqrt(5)} > 10^{999}$$

If we try to solve n:
$$ n*log(\phi) - \frac{log(5)}{2} > 999*log(10) $$
$$ n > \frac{999*log(10)+\frac{log(5)}{2}}{log(\phi)} $$

This gives us that $n > 4781.859..$, so the first index to verify this is $4782$.


```python
def first_n_digit_fibonacci_number_bruteforce(n: int) -> int:
    import math

    second_to_last_number = last_number = 1
    index = 2
    while math.log10(last_number)+1 < n:
        last_number = second_to_last_number + last_number
        second_to_last_number = last_number - second_to_last_number
        index += 1
    print(last_number, second_to_last_number, index)
    return index


def first_n_digit_fibonacci_number_math(n: int) -> int:
    import math

    phi = ( 1 + math.sqrt(5) ) / 2
    return math.ceil(((n-1) * math.log(10) + math.log(5)/2)/math.log(phi))
# END Solution


from IPython.display import  Markdown

N = 1_000
solution = first_n_digit_fibonacci_number_math(n=N)

Markdown(f"""
## Solution

First fibonacci number with {N}-digits: {solution}
""")
```





## Solution

First fibonacci number with 1000-digits: 4782



