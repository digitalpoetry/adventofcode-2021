from aoc.day07 import part1, part2

input_data = """16,1,2,0,4,2,7,1,2,14"""


def test_part1():
    assert part1(input_data) == 37


def test_part2():
    assert part2(input_data) == 168
