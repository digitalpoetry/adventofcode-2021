import re
from typing import Tuple

from aocd.models import Puzzle


def hits_target(dx, dy, current_position: Tuple[int, int],
                target: Tuple[int, int, int, int]) -> bool:
    x, y = current_position
    x_min, x_max, y_min, y_max = target
    if x_min <= x <= x_max and y_min <= y <= y_max:
        return True
    if x > x_max or y < y_min:
        return False
    return hits_target(max(0, dx - 1), (dy - 1), (x + dx, y + dy), target)


def parse(input_data: str) -> Tuple[int, int, int, int]:
    x_min, x_max, y_min, y_max = map(int, re.findall(r'[-\d]+', input_data))
    return x_min, x_max, y_min, y_max


def part1(input_data: str) -> int:
    _, _, y_min, _ = parse(input_data)
    return abs(y_min) * abs(y_min + 1) // 2


def part2(input_data: str) -> int:
    x_min, x_max, y_min, y_max = parse(input_data)
    count = 0
    for dx in range(1, x_max + 1):
        for dy in range(y_min, abs(y_min)):
            if hits_target(dx, dy, (0, 0), (x_min, x_max, y_min, y_max)):
                count += 1
    return count


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=17)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
