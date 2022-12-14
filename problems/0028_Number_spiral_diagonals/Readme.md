# Problem 28: Number spiral diagonals

## Problem

Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

<pre>
<b>21</b> 22 23 24 <b>25</b>
20  <b>7</b>  8  <b>9</b> 10
19  6  <b>1</b>  2 11
18  <b>5</b>  4  <b>3</b> 12
<b>17</b> 16 15 14 <b>13</b>
</pre>

It can be verified that the sum of the numbers on the diagonals is 101.

What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?

## Implementation


```python
# Solution
def sum_spiral_diagonal(size: int) -> int:
    total = 1
    current = 1
    for i in range(int((size-1)/2)):
        inc = 2*(i+1)
        for j in range(4):
            current += inc
            total += current
    return total
# END solution

from IPython.display import  Markdown

SIZE = 1001
# SIZE = 5
solution = sum_spiral_diagonal(size=SIZE)

Markdown(f"""
## Solution

Sum of the numbers of a diagonal of {SIZE}x{SIZE}: {solution}
""")
```





## Solution

Sum of the numbers of a diagonal of 1001x1001: 669171001



