from dataclasses import dataclass
from typing import Set, Any, List, Tuple

from aocd.models import Puzzle


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __post_init__(self):
        if (self.x and self.x < 0) or (self.y and self.y < 0):
            raise ValueError('Unexpected negative value.')


@dataclass(frozen=True)
class Line:
    axis: str
    val: int

    def __post_init__(self):
        if self.axis not in ['x', 'y']:
            raise ValueError("axis must be one of ['x', 'y'].")
        if self.val < 0:
            raise ValueError('Unexpected negative value.')


def parse(input_data: str) -> Tuple[Set[Point], List[Line]]:
    points_input, fold_input = input_data.split('\n\n')
    points: Set[Point] = set()
    for line in points_input.splitlines():
        x, y = map(int, line.split(','))
        points.add(Point(x, y))
    folds: List[Line] = []
    for line in fold_input.splitlines():
        assert line.startswith('fold along ')
        axis, val = line.split()[-1].split('=')
        folds.append(Line(axis, int(val)))
    return points, folds


def xor(a: Any, b: Any) -> bool:
    return bool(a) != bool(b)


def points_to_str(points: Set[Point]) -> str:
    x_max = max(p.x for p in points)
    y_max = max(p.y for p in points)
    plane = [['.' for _ in range(x_max + 1)] for _ in range(y_max + 1)]
    for p in points:
        plane[p.y][p.x] = '#'
    return '\n'.join(''.join(y) for y in plane)


def collapse(point: Point, along: Line) -> Point:
    if along.axis == 'x':
        return Point((along.val - abs(point.x - along.val)), point.y)
    if along.axis == 'y':
        return Point(point.x, (along.val - abs(point.y - along.val)))
    raise ValueError(f'axis {along.axis=} not implemented')


def part1(input_data: str) -> int:
    points, folds = parse(input_data)
    first_fold = next(iter(folds))
    points = set(collapse(p, first_fold) for p in points)
    return len(points)


def part2(input_data: str) -> str:
    points, folds = parse(input_data)
    for fold in folds:
        points = set(collapse(p, fold) for p in points)
    return points_to_str(points)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=13)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
