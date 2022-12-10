# Problem 19: Counting Sundays

## Problem

You are given the following information, but you may prefer to do some research for yourself.

- 1 Jan 1900 was a Monday.
- Thirty days has September,
April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
- A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.
How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?


## Implementation


```python
# Solution

def count_sundays_without_libs() -> int:
    first_of_month_dow = 1  # 1 Jan 1900 is Monday
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    total_count = 0
    for year in range (1900, 2001):
        leap_year = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))
        days_per_month[1] = 29 if leap_year else 28
        for month in range(12):
            if first_of_month_dow == 0 and year >= 1901:
                # print(f"Sunday first of month: {year}-{month+1:02d}-01")
                total_count += 1
            first_of_month_dow = (first_of_month_dow + days_per_month[month]) % 7
    return total_count

def count_sundays_with_libs() -> int:
    from itertools import product
    from datetime import date

    return sum(date(y, m, 1).isoweekday() == 7 for y, m in product(range(1901, 2001), range(1, 13)))

# END Solution


from IPython.display import  Markdown

solution = count_sundays_without_libs()
# solution = count_sundays_with_libs()

Markdown(f"""
## Solution

First of month sunday in the 20th century: {solution}
""")
```





## Solution

First of month sunday in the 20th century: 171



