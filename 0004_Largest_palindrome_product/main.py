def is_palindrome(n: int) -> bool:
    return str(n) == ''.join(list(reversed([c for c in str(n)])))


def get_largest_palindrome(lower_limit: int, upper_limit: int) -> tuple[int, tuple[int, int]]:
    largest_palindrome = 1
    factors = (1, 1)
    for i in range(lower_limit, upper_limit+1):
        for j in range(lower_limit, i+1):
            res = i*j
            if res > largest_palindrome and is_palindrome(res):
                largest_palindrome = res
                factors = (i, j)
    return largest_palindrome, factors


def main():
    largest_palindrome, factors = get_largest_palindrome(100, 999)
    print(f"Largest palindrome product of two 3-digit numbers: {largest_palindrome} (factors={factors})")


if __name__ == "__main__":
    main()
