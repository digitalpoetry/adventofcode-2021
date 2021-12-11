from typing import Dict

from aocd.models import Puzzle


def part1(input_data: str) -> int:
    positions = [int(n) for n in input_data.split(',')]
    return fuel_use(positions, move_cost=lambda x: x)


def part2(input_data: str) -> int:
    positions = [int(n) for n in input_data.split(',')]
    return fuel_use(positions, move_cost=triangle_number)


def fuel_use(positions, move_cost=lambda x: x):
    low, high = min(positions), max(positions) + 1
    # fuel[i] is the fuel required to align all crabs to position i
    fuel: Dict[int, int] = {i: 0 for i in range(low, high)}
    for p in positions:
        for target in range(low, high):
            fuel[target] += move_cost(abs(p - target))
    return min(fuel.values())


def triangle_number(n: int) -> int:
    """
    0, 1, 3, 6, 10, ...
    """
    return n * (n + 1) // 2


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=7)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
