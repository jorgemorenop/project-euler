def sum_multiples(upper_limit: int, factors: list[int]):
    return sum(
        filter(
            lambda n: any([n % factor == 0 for factor in factors]), range(upper_limit)
        )
    )


def main():
    print(f"Sum of multiple of 3 and 5 below 10: {sum_multiples(10, [3, 5])}")
    print(f"Sum of multiple of 3 and 5 below 1000: {sum_multiples(1000, [3, 5])}")


if __name__ == "__main__":
    main()
