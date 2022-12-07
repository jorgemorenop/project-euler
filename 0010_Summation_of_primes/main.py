import math


def sum_primes(upper_limit: int) -> int:
    primes = [2]

    i = 3
    while i < upper_limit:
        is_prime = True
        sqrt_i = math.sqrt(i)
        for p in primes:
            if p > sqrt_i:
                break
            if i % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
        i += 2
    return sum(primes)


def main():
    upper_limit = 2_000_000
    print(f"The sum of all primes below {upper_limit} is {sum_primes(upper_limit)}")


if __name__ == "__main__":
    main()
