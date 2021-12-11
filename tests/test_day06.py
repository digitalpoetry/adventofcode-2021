from aoc.day06 import part1, part2

input_data = """3,4,3,1,2"""


def test_part1():
    assert part1(input_data) == 5934


def test_part2():
    assert part2(input_data) == 26984457539
