from aoc.day21 import part1, part2

input_data = """Player 1 starting position: 4
Player 2 starting position: 8
"""


def test_part1():
    assert part1(input_data) == 739785


def test_part2():
    assert part2(input_data) == 444356092776315
