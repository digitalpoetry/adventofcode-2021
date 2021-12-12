from aoc.day12 import part1, part2, is_large_cave, can_visit_part2

input_data_1 = """start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

input_data_2 = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

input_data_3 = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""


def test_part1():
    assert part1(input_data_1) == 10
    assert part1(input_data_2) == 19
    assert part1(input_data_3) == 226


def test_part2():
    assert part2(input_data_1) == 36
    assert part2(input_data_2) == 103
    assert part2(input_data_3) == 3509


def test_cave_is_lower():
    assert is_large_cave('A')
    assert is_large_cave('BBBB')
    assert not is_large_cave('a')
    assert not is_large_cave('bbbb')
