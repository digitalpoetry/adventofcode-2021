from aoc.day05 import part1, part2, Line, Point

input_data = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


def test_part1():
    assert part1(input_data) == 5


def test_part2():
    assert part2(input_data) == 12


def test_walk():
    line = Line.from_string('1,1 -> 3,1')
    assert {Point(1, 1), Point(2, 1), Point(3, 1)} == set(line.walk())

    line = Line.from_string('5,2 -> 5,1')
    assert {Point(5, 2), Point(5, 1)} == set(line.walk())

    line = Line.from_string('0,0 -> 3,3')
    assert {Point(0, 0), Point(1, 1),
            Point(2, 2), Point(3, 3)} == set(line.walk())

    line = Line.from_string('2,2 -> 0,0')
    assert {Point(2, 2), Point(1, 1), Point(0, 0)} == set(line.walk())
