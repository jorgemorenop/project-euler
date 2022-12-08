def longest_collatz_sequence(upper_limit: int) -> int:
    return 0


def main():
    upper_limit = 1_000_000
    print(
        f"The starting number, under {upper_limit}, that produces the longest chain is: "
        f"{longest_collatz_sequence(upper_limit)}"
    )


if __name__ == "__main__":
    main()
