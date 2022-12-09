# Problem 15: Lattice paths

## Problem

Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

![](example_grid_2x2.png)

How many such routes are there through a 20×20 grid?


## Implementation


```python
import math
from IPython.display import Markdown as md


def lattice_paths(grid_size: int) -> int:
    # Path is a 2 * N ordered sequence with N move-right and N move-down steps
    res = int(math.factorial(2*grid_size)/(math.factorial(grid_size)**2))
    return res


grid_size = 20
md(f"""
## Solution

Routes in a {grid_size}x{grid_size} grid: {lattice_paths(grid_size=20)}
""")
```





## Solution

Routes in a 20x20 grid: 137846528820



