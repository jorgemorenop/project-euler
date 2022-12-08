from pathlib import Path


def names_scores(names: list[str]) -> int:
    res = 0

    print(f"Sum of all name scores: {res}")
    return res


if __name__ == "__main__":
    with (Path(__file__).parent / "names.txt").open('r') as f:
        names_scores(names=[e.strip('"') for e in f.read().split(',')])
