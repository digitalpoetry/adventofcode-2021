from aoc.day15 import part1, part2, grow_input

input_data = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""

input_data_custom1 = """199999
191119
191911
111991
"""

input_data_custom2 = "8"


def test_part1():
    assert part1(input_data) == 40
    assert part1(input_data_custom1) == 12


def test_part2():
    assert part2(input_data) == 315


def test_grow_input():
    assert grow_input(input_data_custom2) == """89123
91234
12345
23456
34567"""
