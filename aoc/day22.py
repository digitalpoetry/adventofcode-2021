import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from aocd.models import Puzzle


@dataclass(frozen=True)
class Cuboid:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    @staticmethod
    def from_string(s: str) -> 'Cuboid':
        c = Cuboid(*map(int, re.findall(r'[-\d]+', s)))
        assert c.is_valid(), 'min-max pairs must be sorted'
        return c

    def intersection(self, other: 'Cuboid') -> Optional['Cuboid']:
        c = Cuboid(
            max(self.x_min, other.x_min),
            min(self.x_max, other.x_max),
            max(self.y_min, other.y_min),
            min(self.y_max, other.y_max),
            max(self.z_min, other.z_min),
            min(self.z_max, other.z_max),
        )
        if c.is_valid():
            return c
        return None

    def is_valid(self) -> bool:
        return (self.x_min <= self.x_max and self.y_min <= self.y_max
                and self.z_min <= self.z_max)

    def volume(self) -> int:
        return ((self.x_max - self.x_min + 1) * (self.y_max - self.y_min + 1) *
                (self.z_max - self.z_min + 1))


def reboot(input_data: str, window: Cuboid = None) -> int:
    lit: Counter[Cuboid] = Counter()

    for line in input_data.splitlines():
        command, xyz = line.split()
        change = Cuboid.from_string(xyz)

        if window and change.intersection(window) is None:
            continue

        # Create a void at all intersections with existing cuboids
        void: Counter[Cuboid] = Counter()
        for lit_cuboid, count in lit.items():
            if intersection := change.intersection(lit_cuboid):
                void[intersection] -= count
        lit.update(void)

        if command == 'on':
            lit[change] += 1

    return sum(count * cuboid.volume() for cuboid, count in lit.items())


def part1(input_data: str) -> int:
    return reboot(input_data, window=Cuboid(-50, 50, -50, 50, -50, 50))


def part2(input_data: str) -> int:
    return reboot(input_data)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=22)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
