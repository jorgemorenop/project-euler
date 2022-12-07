def find_pythagorean_triplet_product(total_sum: int) -> int:
    a = 1
    max_a = total_sum / 3   # since a < b < c
    while a < max_a:
        a_squared = a ** 2
        b = a + 1
        max_b = (total_sum - a) / 2     # since b < c
        while b < max_b:
            c = total_sum - a - b
            if a_squared + b**2 == c**2:
                return a*b*c
            b += 1
        a += 1
    raise ArithmeticError(f"No Pythagorean triplet for a + b + c = {total_sum}")


def main():
    total_sum = 1000
    print(
        f"The product abc for a Pythagorean triplet that verifies a+b+c=1000 is: "
        f"{find_pythagorean_triplet_product(total_sum)}"
    )


if __name__ == "__main__":
    main()
