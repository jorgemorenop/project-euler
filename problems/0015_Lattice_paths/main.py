import math


def lattice_paths(grid_size: int) -> int:
    # Path is a 2 * N ordered sequence with N move-right and N move-down steps
    res = int(math.factorial(2*grid_size)/(math.factorial(grid_size)**2))
    print(f"Routes in a {grid_size}x{grid_size} grid: {res}")
    return res


if __name__ == "__main__":
    lattice_paths(grid_size=20)
