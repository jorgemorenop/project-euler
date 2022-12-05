def get_factors(n: int):
    factors = []
    i = 2
    while i < n:
        while n % i == 0:
            n = n / i
            factors.append(i)
        i += 1
    factors.append(int(n))
    return sorted(factors)


def main():
    n = 600851475143
    factors = get_factors(n)
    print(f"Largest prime factor of {n}: {max(factors)} (All prime factors: {factors})")


if __name__ == "__main__":
    main()
