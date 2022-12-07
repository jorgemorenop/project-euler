import math


def nth_prime(n: int) -> int:
    primes = [2]

    i = 3
    while len(primes) < n:
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
    return primes[n-1]


def main():
    n = 10001
    print(f"The {n}-th prime is: {nth_prime(n)}")


if __name__ == "__main__":
    main()
