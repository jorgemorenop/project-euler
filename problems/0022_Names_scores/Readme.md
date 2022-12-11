# Problem 22: Names scores

## Problem

Using [names.txt](names.txt) (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938 × 53 = 49714.

What is the total of all the name scores in the file?



## Implementation


```python
from pathlib import Path

# Solution
def names_scores(names: list[str]) -> int:
    return sum(sum(ord(c) - ord('A') + 1 for c in name.upper()) * (i+1) for i, name in enumerate(sorted(names)))
# END Solution


from IPython.display import  Markdown

with Path("names.txt").open('r') as f:
    solution = names_scores(names=[e.strip('"') for e in f.read().split(',')])

Markdown(f"""
## Solution

Sum of all name scores: {solution}
""")
```





## Solution

Sum of all name scores: 871198282



