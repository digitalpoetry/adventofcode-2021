from aoc.day14 import part1, part2

input_data = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""


def test_part1():
    assert part1(input_data) == 1588


def test_part2():
    assert part2(input_data) == 2188189693529
