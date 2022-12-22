# Problem 42: Coded triangle numbers

## Problem

The nth term of the sequence of triangle numbers is given by, $t_n = \frac{1}{2}n(n+1)$; so the first ten triangle numbers are:

$$1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...$$


By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is $19 + 11 + 25 = 55 = t_{10}$. If the word value is a triangle number then we shall call the word a triangle word.

Using [words.txt](words.txt) (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?

## Implementation


```python
# Solution
def coded_triangle_numbers(words: list[str]) -> int:
    precalculated_max_score = 300

    triangle_numbers = [1]
    while triangle_numbers[-1] < precalculated_max_score:
        n = len(triangle_numbers) + 1
        triangle_numbers.append(n*(n+1)/2)

    def is_word_triangle(word: str) -> bool:
        return sum([ord(c) - ord('A') + 1 for c in word.upper()]) in triangle_numbers

    return sum(map(is_word_triangle, words))
# END solution


from IPython.display import  Markdown
from pathlib import Path

with Path("words.txt").open('r') as f:
    solution = coded_triangle_numbers(words=[e.strip('"') for e in f.read().split(',')])

Markdown(f"""
## Solution

Number of triangle words: {solution}
""")
```





## Solution

Number of triangle words: 162



