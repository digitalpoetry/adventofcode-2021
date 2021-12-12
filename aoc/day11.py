import itertools
from dataclasses import dataclass
from typing import Dict, List

from aocd.models import Puzzle


@dataclass(frozen=True)
class Coord:
    row: int
    col: int


@dataclass
class Octopus:
    energy_level: int
    has_flashed: bool = False

    def increment_energy(self) -> None:
        self.energy_level += 1

    def is_ready_to_flash(self):
        return not self.has_flashed and self.energy_level > 9

    def reset_if_flashed(self) -> bool:
        if self.has_flashed:
            self.energy_level = 0
            self.has_flashed = False
            return True
        return False


def parse(input_data) -> Dict[Coord, Octopus]:
    return {
        Coord(row, col): Octopus(int(digit))
        for row, line in enumerate(input_data.splitlines())
        for col, digit in enumerate(line)
    }


def get_adjacent_coords(coord: Coord) -> List[Coord]:
    product = itertools.product((-1, 0, 1), repeat=2)
    delta = (p for p in product if p != (0, 0))
    return [Coord(coord.row + d[0], coord.col + d[1]) for d in delta]


def try_flash(cave: Dict[Coord, Octopus], coord: Coord) -> int:
    o = cave[coord]
    if not o.is_ready_to_flash():
        return 0
    o.has_flashed = True
    total_flashes = 1
    for a in get_adjacent_coords(coord):
        if a not in cave:
            continue
        cave[a].increment_energy()
        total_flashes += try_flash(cave, a)
    return total_flashes


def part1(input_data: str) -> int:
    cave = parse(input_data)
    total_flashes = 0
    for i in range(100):
        # The energy level of each octopus increases by 1.
        for o in cave.values():
            o.increment_energy()
        # Any octopus with an energy level greater than 9 flashes.
        for coord in cave.keys():
            total_flashes += try_flash(cave, coord)
        # Any octopus that flashed during this step has its energy level set to 0.
        for o in cave.values():
            o.reset_if_flashed()
    return total_flashes


def part2(input_data: str) -> int:
    cave = parse(input_data)
    iteration = 0
    while True:
        iteration += 1
        # The energy level of each octopus increases by 1.
        for o in cave.values():
            o.increment_energy()
        # Any octopus with an energy level greater than 9 flashes.
        for coord in cave.keys():
            try_flash(cave, coord)
        # Any octopus that flashed during this step has its energy level set to 0.
        resets = [o.reset_if_flashed() for o in cave.values()]
        if all(resets):
            return iteration


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=11)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
