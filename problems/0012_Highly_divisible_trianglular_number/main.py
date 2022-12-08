import math


def get_divisors(n: int):
    divisors = {1, n}
    for i in range(1, int(math.sqrt(n))+1):
        if n % i == 0:
            divisors.update({i, int(n/i)})
    return divisors


def highly_divisible_triangular_number(target_number_of_divisors: int, verbose: bool = False) -> int:
    n = i = 1
    n_divisors = 1
    while n_divisors < target_number_of_divisors:
        i += 1
        n += i
        divisors = get_divisors(n)
        n_divisors = len(get_divisors(n))
        if verbose:
            print(f"{n}: {n_divisors} divisors ({sorted(divisors)})")
    return n


def main():
    target_number_of_divisors = 500

    print(
        f"The first triangle number to have over {target_number_of_divisors} divisors is: "
        f"{highly_divisible_triangular_number(target_number_of_divisors)}"
    )


if __name__ == "__main__":
    main()
