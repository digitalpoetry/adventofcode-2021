from aoc.day01 import part1, part2

input_data = """199
200
208
210
200
207
240
269
260
263
"""


def test_part1():
    assert part1(input_data) == 7


def test_part2():
    assert part2(input_data) == 5
