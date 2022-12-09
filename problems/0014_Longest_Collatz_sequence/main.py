def longest_collatz_sequence(upper_limit: int) -> int:
    steps_per_sequence = {}
    max_steps = 0
    longest_sequence_start = 0
    for i in range(1, upper_limit+1):
        n = i
        current_steps = 1
        while n != 1:
            if n in steps_per_sequence:
                current_steps += steps_per_sequence[n]
                break
            n = n / 2 if n % 2 == 0 else 3*n + 1
            current_steps += 1
        if current_steps > max_steps:
            max_steps = current_steps
            longest_sequence_start = i
        steps_per_sequence[i] = current_steps
    return longest_sequence_start


def main():
    upper_limit = 1_000_000
    print(
        f"The starting number, under {upper_limit}, that produces the longest chain is: "
        f"{longest_collatz_sequence(upper_limit)}"
    )


if __name__ == "__main__":
    main()
