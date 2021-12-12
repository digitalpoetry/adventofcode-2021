from aoc.day11 import part1, part2

input_data = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""


def test_part1():
    assert part1(input_data) == 1656


def test_part2():
    assert part2(input_data) == 195
