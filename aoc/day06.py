from typing import List

from aocd.models import Puzzle


def part1(input_data: str) -> int:
    return model(input_data, iterations=80)


def part2(input_data: str) -> int:
    return model(input_data, iterations=256)


def model(input_data: str, iterations: int = 80) -> int:
    # fish[i] represents the number of fish with internal timer i.
    fish: List[int] = [0] * 9
    for timer in (int(n) for n in input_data.split(',')):
        fish[timer] += 1
    day = 0
    while day < iterations:
        mitosing, *rest = fish
        rest[6] += mitosing
        fish = rest + [mitosing]
        assert len(fish) == 9, "invariant: len(fish) must always be 9"
        day += 1
    return sum(fish)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=6)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
