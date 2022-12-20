# Problem 39: Integer right triangles

## Problem

If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.

{20,48,52}, {24,45,51}, {30,40,50}

For which value of p ≤ 1000, is the number of solutions maximised?

## Implementation

We have the following equations:

$$a+b+c=p$$

$$a^2+b^2=c^2$$

If we substitute the value of $c$ in the first equation with its value in the 2nd equation we get:

$$a+b+\sqrt{a^2+b^2}=p$$

After some mathematical manipulations we can write $b$ as a function of $a$ and $p$:

$$b = \frac{p\cdot (a-\frac{p}{2})}{a-p}$$

So we just have to loop over the possible values of $p$ and $a < \frac{p}{3}$ and retrieve the solutions where b is integer.


```python
# Solution
def integer_right_triangles(upper_limit: int) -> int:
    max_sols = 0
    max_sols_p = 0
    for p in range(3, upper_limit+1):
        p_sols = 0
        for a in range(1, p):
            b = p*(a-p/2)/(a-p)
            if b.is_integer() and 0<b<=a:
                p_sols += 1
                if p_sols > max_sols:
                    max_sols_p = p
                    max_sols = p_sols
    return max_sols_p
# END solution

from IPython.display import  Markdown

solution = integer_right_triangles(upper_limit=1000)

Markdown(f"""
## Solution

Value P with most solutions: {solution}
""")
```





## Solution

Value P with most solutions: 840



