def longest_collatz_sequence(upper_limit: int) -> int:
    steps_per_sequence = {}
    max_steps = 0
    longest_sequence_start = 0
    for i in range(1, upper_limit+1):
        n = i
        current_sequence = [n]
        n_steps = None
        while n != 1:
            if n in steps_per_sequence:
                n_steps = len(current_sequence) + steps_per_sequence[n]
                break
            n = n / 2 if n % 2 == 0 else 3*n + 1
            current_sequence.append(n)
        if not n_steps:
            n_steps = len(current_sequence)
        for step_i, step_number in enumerate(current_sequence):
            steps_per_sequence[step_number] = n_steps - step_i
        if n_steps > max_steps:
            max_steps = n_steps
            longest_sequence_start = i
    return longest_sequence_start


def main():
    upper_limit = 1_000_000
    print(
        f"The starting number, under {upper_limit}, that produces the longest chain is: "
        f"{longest_collatz_sequence(upper_limit)}"
    )


if __name__ == "__main__":
    main()
