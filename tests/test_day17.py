from aoc.day17 import part1, part2

input_data = """target area: x=20..30, y=-10..-5"""


def test_part1():
    assert part1(input_data) == 45


def test_part2():
    assert part2(input_data) == 112
