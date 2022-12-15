# Problem 31: Coin sums

## Problem

In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in general circulation:

1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).
It is possible to make £2 in the following way:

1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p
How many different ways can £2 be made using any number of coins?

## Implementation


```python
# Solution
def coin_sums(qt: int) -> int:
    def use_coins(available_coins: set[int], current_qt: int) -> int:
        if not available_coins:
            return 0

        if len(available_coins) == 1:
            return int(current_qt % available_coins.pop() == 0)

        n = 0
        coin = max(available_coins)
        coin_qt = 0
        while coin_qt < current_qt:
            n += use_coins(available_coins-{coin}, current_qt-coin_qt)
            coin_qt += coin
            if coin_qt == current_qt:
                n += 1
        return n

    return use_coins({1, 2, 5, 10, 20, 50, 100, 200}, qt)
# END solution

from IPython.display import  Markdown

QT = 200
solution = coin_sums(qt=QT)

Markdown(f"""
## Solution

Number of ways to get {QT}p: {solution}
""")
```





## Solution

Number of ways to get 200p: 73682



