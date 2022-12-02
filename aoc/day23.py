import re
from dataclasses import dataclass
from typing import Optional

from aocd.models import Puzzle

"""
A amphipods are assigned a value of 0, energy = 1 * 10^0
B amphipods are assigned a value of 0, energy = 1 * 10^1
C amphipods are assigned a value of 0, energy = 1 * 10^2
D amphipods are assigned a value of 0, energy = 1 * 10^3
"""

Hall = tuple[Optional[int], ...]
Room = tuple[Optional[int], ...]
Rooms = tuple[Room, Room, Room, Room]

EMPTY_HALL: Hall = (None,) * 11


@dataclass(frozen=True)
class State:
    rooms: Rooms
    hall: Hall = (None,)
    energy: int = 0

    @property
    def is_organised(self):
        hall_is_empty = all(h is None for h in self.hall)
        amphipods_are_home = all(
            all(amphipod == i for amphipod in room)
            for i, room in enumerate(self.rooms)
        )
        return hall_is_empty and amphipods_are_home


def parse(input_data: str, *, part: int) -> Rooms:
    assert part in (1, 2)

    amphipod_queue: list[list[str]] = []
    for line in input_data.splitlines():
        amphipods = re.findall(r'[ABCD]', line)
        if amphipods:
            amphipod_queue.append(amphipods)
    if part == 2:
        amphipod_queue.append(['D', 'C', 'B', 'A'])
        amphipod_queue.append(['D', 'B', 'A', 'C'])

    return (
        tuple(ord(a) - ord("A") for a, b, c, d in amphipod_queue),
        tuple(ord(b) - ord("A") for a, b, c, d in amphipod_queue),
        tuple(ord(c) - ord("A") for a, b, c, d in amphipod_queue),
        tuple(ord(d) - ord("A") for a, b, c, d in amphipod_queue),
    )


def solve(state: State) -> State:
    pass


def part1(input_data: str) -> int:
    rooms = parse(input_data, part=1)
    solution_state = solve(State(rooms, EMPTY_HALL))
    return solution_state.energy


def part2(input_data: str) -> int:
    rooms = parse(input_data, part=2)
    solution_state = solve(State(rooms, EMPTY_HALL))
    return solution_state.energy


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=23)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
