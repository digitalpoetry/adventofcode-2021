from aoc.day23 import part1, part2

input_data = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""


def test_part1():
    assert part1(input_data) == 12521


def test_part2():
    assert part2(input_data) == 44169
