from dataclasses import dataclass
from typing import Dict, Union

from aocd.models import Puzzle


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def add(self, delta: 'Position') -> 'Position':
        return Position(self.x + delta.x, self.y + delta.y)

    def scale(self, scalar: Union[int, str]) -> 'Position':
        return Position(self.x * int(scalar), self.y * int(scalar))


direction_map: Dict[str, Position] = {
    'forward': Position(1, 0),
    'down': Position(0, 1),
    'up': Position(0, -1),
}


def part1(input_data: str) -> int:
    current_position = Position()
    for line in input_data.splitlines():
        command, scalar = line.split()
        delta = direction_map[command].scale(scalar)
        current_position = current_position.add(delta)
    return current_position.x * current_position.y


def part2(input_data: str) -> int:
    current_position = Position()
    aim = 0
    for line in input_data.splitlines():
        command, scalar = line.split()
        scalar = int(scalar)
        if command == 'down':
            aim += scalar
        elif command == 'up':
            aim -= scalar
        elif command == 'forward':
            current_position = current_position.add(
                Position(scalar, aim * scalar))
    return current_position.x * current_position.y


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=2)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
