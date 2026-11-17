# Problem 55: Lychrel Numbers

## Problem

If we take $47$, reverse and add, $47 + 74 = 121$, which is palindromic.

Not all numbers produce palindromes so quickly. For example,

$$\begin{align}
349 + 943 &= 1292\\
1292 + 2921 &= 4213\\
4213 + 3124 &= 7337
\end{align}$$

That is, $349$ took three iterations to arrive at a palindrome.

Although no one has proved it yet, it is thought that some numbers, like $196$, never produce a palindrome. A number that never forms a palindrome through the reverse and add process is called a Lychrel number. Due to the theoretical nature of these numbers, and for the purpose of this problem, we shall assume that a number is Lychrel until proven otherwise. In addition you are given that for every number below ten-thousand, it will either (i) become a palindrome in less than fifty iterations, or, (ii) no one, with all the computing power that exists, has managed so far to map it to a palindrome. In fact, $10677$ is the first number to be shown to require over fifty iterations before producing a palindrome: $4668731596684224866951378664$ ($53$ iterations, $28$-digits).

Surprisingly, there are palindromic numbers that are themselves Lychrel numbers; the first example is $4994$.

How many Lychrel numbers are there below ten-thousand?

NOTE: Wording was modified slightly on 24 April 2007 to emphasise the theoretical nature of Lychrel numbers.


## Implementation


```python
# Solution
import time

def is_palindrome(number: int) -> bool:
    return str(number) == str(number)[::-1]

def reverse_add(number: int) -> int:
    return number + int(str(number)[::-1])

def lychrel_numbers(max_n: int = 10000, max_iterations: int = 50) -> int:
    start_ts = time.perf_counter()
    palindrome_producers = set()
    lychrel_number_producers = set()
    lychrel_numbers = set()
    for n in range(max_n, 0, -1):
        current_iteration = []
        is_lychrel = True
        i = 0
        p = n
        while i < max_iterations:
            p = reverse_add(p)
            current_iteration.append(p)
            if is_palindrome(p) or p in palindrome_producers:
                palindrome_producers.update(current_iteration)
                is_lychrel = False
                break
            if p in lychrel_number_producers:
               break
            i += 1
        if is_lychrel:
            lychrel_number_producers.update(current_iteration)
            lychrel_numbers.add(n)
        # print(f"{n} {'is' if is_lychrel else 'is not'} Lychrel number: + {current_iteration}")
    print(f"Lychrel numbers: {lychrel_numbers}")
    print(f"Time taken: {time.perf_counter() - start_ts}")
    return len(lychrel_numbers)
# END solution


from IPython.display import  Markdown

solution = lychrel_numbers()

Markdown(f"""
## Solution

How many Lychrel numbers are there below ten-thousand?: {solution}
""")
```

    Lychrel numbers: {8705, 3585, 8709, 7689, 4619, 6670, 8719, 6672, 9237, 6167, 2584, 7706, 2586, 9254, 5671, 5673, 9258, 8238, 5168, 9777, 1585, 6707, 9268, 1587, 8760, 8255, 4672, 9794, 8259, 4674, 9798, 7239, 4169, 8778, 5708, 8269, 9808, 7761, 592, 7256, 3673, 8795, 3675, 8799, 7779, 4709, 6760, 8809, 6762, 9327, 6257, 2674, 7796, 2676, 9344, 5761, 5763, 9348, 8328, 5258, 9867, 1675, 6797, 9358, 1677, 8850, 8345, 4762, 9884, 8349, 4764, 9888, 7329, 4259, 8868, 5798, 8359, 9898, 7851, 689, 7346, 3763, 691, 8885, 3765, 8889, 7869, 4799, 6850, 8899, 6852, 196, 9417, 6347, 2764, 7886, 2766, 9434, 5851, 5853, 9438, 8418, 5348, 9957, 1765, 6887, 9448, 1767, 8940, 8435, 4852, 9974, 8439, 4854, 9978, 7419, 4349, 8958, 5888, 8449, 9988, 7941, 7436, 3853, 9999, 8975, 3855, 8979, 788, 790, 7959, 4889, 6940, 8989, 8990, 6942, 9507, 6437, 2854, 295, 7976, 2856, 8490, 9524, 5941, 7991, 9528, 5943, 8508, 5438, 1855, 6977, 9538, 7491, 1857, 8525, 4942, 6992, 8529, 4944, 7509, 4439, 6490, 8539, 6492, 5978, 9057, 7526, 3943, 5993, 3945, 879, 9074, 5491, 4979, 5493, 9078, 887, 8058, 9597, 6527, 9088, 2944, 4994, 2946, 8580, 394, 8075, 4492, 9614, 8079, 4494, 9618, 7059, 8598, 5528, 8089, 1945, 3995, 9628, 7581, 1947, 7076, 3493, 8615, 3495, 8619, 7599, 4529, 6580, 8629, 6582, 2996, 9147, 6077, 2494, 7616, 2496, 9164, 5581, 1997, 5583, 9168, 978, 8148, 5078, 9687, 1495, 6617, 9178, 1497, 986, 8670, 8165, 4582, 9704, 8169, 4584, 9708, 7149, 493, 4079, 8688, 5618, 8179, 9718, 7671, 7166, 3583}
    Time taken: 0.004775082925334573






## Solution

How many Lychrel numbers are there below ten-thousand?: 249



