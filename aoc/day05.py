import itertools
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Iterable, Generator, Any, Iterator

from aocd.models import Puzzle


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Line:
    start: Point
    end: Point

    @staticmethod
    def from_string(line: str) -> 'Line':
        x1, y1, x2, y2 = (int(n) for n in line.replace(' -> ', ',').split(','))
        return Line(Point(x1, y1), Point(x2, y2))

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def is_diagonal(self) -> bool:
        return abs(self.start.x - self.end.x) == abs(self.start.y - self.end.y)

    def walk(self) -> Generator[Point, Any, None]:
        if self.is_horizontal():
            leftmost, rightmost = sorted((self.start.x, self.end.x))
            return (Point(x, self.start.y)
                    for x in range(leftmost, rightmost + 1))
        elif self.is_vertical():
            bottom, top = sorted((self.start.y, self.end.y))
            return (Point(self.start.x, y) for y in range(bottom, top + 1))
        elif self.is_diagonal():
            leftmost, rightmost = sorted((self.start.x, self.end.x))
            bottom, top = sorted((self.start.y, self.end.y))
            xs = [x for x in range(leftmost, rightmost + 1)]
            ys = [y for y in range(bottom, top + 1)]
            if self.start.x == xs[0] and not self.start.y == ys[0]:
                ys.reverse()
            if self.start.y == ys[0] and not self.start.x == xs[0]:
                xs.reverse()
            return (Point(x, y) for x, y in zip_longest_memo(xs, ys))
        raise NotImplementedError('Unsupported operation')

    def __iter__(self) -> Iterator[Point]:
        return self.walk()


def zip_longest_memo(iter1, iter2):
    iter1_last, iter2_last = None, None
    for a, b in itertools.zip_longest(iter1, iter2, fillvalue=None):
        if a is None:
            a = iter1_last
        if b is None:
            b = iter2_last
        iter1_last, iter2_last = a, b
        yield a, b


def part1(input_data: str):
    lines = (Line.from_string(l) for l in input_data.splitlines())
    point_count: Dict[Point, int] = defaultdict(int)
    for line in lines:
        if not line.is_horizontal() and not line.is_vertical():
            continue
        for point in line:
            point_count[point] += 1
    return sum(1 for p, count in point_count.items() if count > 1)


def part2(input_data: str):
    lines = (Line.from_string(l) for l in input_data.splitlines())
    point_count: Dict[Point, int] = defaultdict(int)
    for line in lines:
        for point in line:
            point_count[point] += 1
    return sum(1 for p, count in point_count.items() if count > 1)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=5)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
