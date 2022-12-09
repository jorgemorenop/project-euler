def power_digit_sum(power: int) -> int:
    res = sum(int(i) for i in str(2**power))
    print(f"Sum of the digits of 2^{power}: {res}")
    return res


if __name__ == "__main__":
    power_digit_sum(power=1000)
