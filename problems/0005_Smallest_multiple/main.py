def smallest_multiple(upper_limit: int):
    n = upper_limit
    while True:
        if all([n % j == 0 for j in range(1, upper_limit+1)]):
            return n
        n += upper_limit


def main():
    print(f"Smallest multiple of all numbers from 1 to 20: {smallest_multiple(20)}")


if __name__ == "__main__":
    main()
