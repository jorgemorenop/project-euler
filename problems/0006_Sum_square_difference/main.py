def sum_square_difference(upper_limit: int):
    sum_of_squares = sum(i**2 for i in range(upper_limit+1))
    square_of_sum = int((upper_limit + 1) * upper_limit / 2) ** 2
    return square_of_sum - sum_of_squares


def main():
    print(f"Difference between sum of the squares and square of sums (first 100 numbers): {sum_square_difference(100)}")


if __name__ == "__main__":
    main()
