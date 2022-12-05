def sum_even_fibonnaci(upper_limit: int):
    second_to_last_number = last_number = 1
    total = 0
    while last_number < upper_limit:
        if last_number % 2 == 0:
            total += last_number

        last_number = second_to_last_number + last_number
        second_to_last_number = last_number - second_to_last_number
    return total


def main():
    print(
        f"Sum of even valued Fibonacci terms (below 4 million): {sum_even_fibonnaci(4_000_000)}"
    )


if __name__ == "__main__":
    main()
