from itertools import pairwise
from typing import Tuple, Generator

from aocd.models import Puzzle


def triplewise(iterable) -> Generator[Tuple, None, None]:
    """
    Return overlapping triplets from an iterable.
    triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    """
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def part1(input_data: str) -> int:
    depths = [int(n) for n in input_data.splitlines()]
    return sum((a < b) for a, b in pairwise(depths))


def part2(input_data):
    depths = [int(n) for n in input_data.splitlines()]
    triplet_sums = (sum(t) for t in triplewise(depths))
    return sum((a < b) for a, b in pairwise(triplet_sums))


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=1)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
