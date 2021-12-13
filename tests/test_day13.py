from aoc.day13 import part1, part2, points_to_str, parse, collapse, Point, Line

input_data = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""


def test_print_grid():
    points, _ = parse(input_data)
    assert points_to_str(points) == """...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........"""


def test_collapse():
    assert collapse(Point(3, 3), Line('x', 2)) == Point(1, 3)
    assert collapse(Point(5, 4), Line('y', 2)) == Point(5, 0)


def test_part1():
    assert part1(input_data) == 17


def test_part2():
    assert part2(input_data) == """#####
#...#
#...#
#...#
#####"""
