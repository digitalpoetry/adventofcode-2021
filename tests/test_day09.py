from aoc.day09 import part1, part2

input_data = """2199943210
3987894921
9856789892
8767896789
9899965678
"""


def test_part1():
    assert part1(input_data) == 15


def test_part2():
    assert part2(input_data) == 1134
