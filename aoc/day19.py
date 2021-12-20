import itertools
from collections import deque
from dataclasses import dataclass
from typing import Optional

from aocd.models import Puzzle
"""
The relative position of beacons within a scanner range is known. We can model these as vectors.
We can then compare the vectors between scanners independent of the coordinate system.
"""


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def manhattan_distance(self, other: 'Point') -> int:
        return (abs(self.x - other.x) + abs(self.y - other.y) +
                abs(self.z - other.z))


@dataclass(frozen=True)
class Vector:
    i: int
    j: int
    k: int

    @staticmethod
    def from_points(a, b: Point) -> 'Vector':
        return Vector(b.x - a.x, b.y - a.y, b.z - a.z)


@dataclass
class Scanner:
    points: list[Point]
    absolute_position: Optional[Point] = None

    def __iter__(self):
        return iter(self.points)

    def all_plane_rotations(self):
        yield Scanner([Point(p.x, p.y, p.z) for p in self.points])
        yield Scanner([Point(p.y, -p.x, p.z) for p in self.points])
        yield Scanner([Point(-p.x, -p.y, p.z) for p in self.points])
        yield Scanner([Point(-p.y, p.x, p.z) for p in self.points])

    def all_space_rotations(self):
        yield Scanner([Point(p.x, p.y, p.z) for p in self.points])
        yield Scanner([Point(p.z, p.y, -p.x) for p in self.points])
        yield Scanner([Point(-p.x, p.y, -p.z) for p in self.points])
        yield Scanner([Point(-p.z, p.y, p.x) for p in self.points])
        yield Scanner([Point(p.x, p.z, -p.y) for p in self.points])
        yield Scanner([Point(p.x, -p.z, p.y) for p in self.points])

    def vectors(self, origin: Point) -> set[Vector]:
        return set(Vector.from_points(origin, p) for p in self.points)

    def has_overlap_with(
        self,
        other: 'Scanner',
        min_overlap: int = 12
    ) -> Optional[tuple['Scanner', tuple[Point, Point]]]:
        for scanner1_origin in self.points[min_overlap - 1:]:
            vector_set1 = self.vectors(scanner1_origin)
            for scanner2_origin in other.points:
                vector_set2 = other.vectors(scanner2_origin)
                if len(vector_set1 & vector_set2) >= min_overlap:
                    return other, (scanner1_origin, scanner2_origin)
        return None

    def has_transpositional_overlap_with(
        self,
        other: 'Scanner',
        min_overlap: int = 12
    ) -> Optional[tuple['Scanner', tuple[Point, Point]]]:
        for space in other.all_space_rotations():
            for plane in space.all_plane_rotations():
                if result := self.has_overlap_with(plane, min_overlap):
                    return result
        return None

    def __contains__(self, item):
        return item in self.points

    @staticmethod
    def align(a, b: 'Scanner', shared_point: tuple[Point, Point]) -> None:
        assert bool(a.absolute_position) != bool(b.absolute_position), \
            'Exactly one scanner\'s absolute_position must be defined'
        if a.absolute_position is None:
            a, b = b, a
        a_point, b_point = shared_point
        assert a_point in a
        assert b_point in b
        diff_x, diff_y, diff_z = (p1 - p2 for p1, p2 in zip(*shared_point))
        b.points = [Point(p.x + diff_x, p.y + diff_y, p.z + diff_z) for p in b]
        b.absolute_position = Point(diff_x, diff_y, diff_z)


def parse(input_data: str) -> list[Scanner]:
    sections = input_data.split('\n\n')
    scanners: list[Scanner] = []
    for section in sections:
        lines = section.splitlines()[1:]
        points: list[Point] = []
        for line in lines:
            x, y, z = (int(n) for n in line.split(','))
            points.append(Point(x, y, z))
        scanners.append(Scanner(points))
    return scanners


def align_scanner_to_first(scanners) -> list[Scanner]:
    scanners[0].absolute_position = Point(0, 0, 0)
    aligned = deque([scanners.pop(0)])
    while scanners:
        print(f'{len(scanners)} waiting for alignment')
        for i, j in itertools.product(range(len(aligned)),
                                      range(len(scanners))):
            reference_scanner = aligned[i]
            test_scanner = scanners[j]
            if result := reference_scanner.has_transpositional_overlap_with(
                    test_scanner):
                transformed_scanner, shared_point = result
                Scanner.align(reference_scanner, transformed_scanner,
                              shared_point)
                aligned.appendleft(transformed_scanner)
                scanners.remove(test_scanner)
                break
        else:
            raise Exception('Could not find any scanner to align')
    return list(aligned)


def part1(input_data: str) -> int:
    scanners = parse(input_data)
    aligned = align_scanner_to_first(scanners)

    all_points = []
    for s in aligned:
        assert s.absolute_position is not None
        all_points.extend(s.points)
    return len(set(all_points))


def part2(input_data: str) -> int:
    scanners = parse(input_data)
    aligned = align_scanner_to_first(scanners)

    max_manhattan_distance = 0
    for s1, s2 in itertools.combinations(aligned, 2):
        assert s1.absolute_position is not None
        assert s2.absolute_position is not None
        dist = s1.absolute_position.manhattan_distance(s2.absolute_position)
        if dist > max_manhattan_distance:
            max_manhattan_distance = dist
    return max_manhattan_distance


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=19)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
