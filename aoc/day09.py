from functools import reduce
from typing import Tuple, List

from aocd.models import Puzzle
from networkx import Graph, grid_2d_graph, connected_components


def parse(input_data: str) -> Graph:
    lines = input_data.splitlines()
    nrow = len(lines)
    ncol = len(next(iter(lines)))
    g: Graph = grid_2d_graph(nrow, ncol)
    for row, line in enumerate(lines):
        for col, digit in enumerate(line):
            n = g.nodes.get((row, col))
            n['height'] = int(digit)
            n['risk'] = n['height'] + 1
    return g


def part1(input_data: str) -> int:
    g = parse(input_data)
    total_risk = 0
    for this, this_attr in g.nodes.items():
        is_low_point = all(g.nodes[neighbour]['height'] > this_attr['height']
                           for neighbour in g.neighbors(this))
        if is_low_point:
            total_risk += this_attr['risk']
    return total_risk


def part2(input_data: str) -> int:
    g = parse(input_data)
    peaks: List[Tuple[int, int]] = []
    for node, node_attr in g.nodes.items():
        if node_attr['height'] == 9:
            peaks.append(node)
    g.remove_nodes_from(peaks)
    components = sorted(connected_components(g), key=len)
    top3 = components[-3:]
    return reduce(lambda x, y: x * y, (len(c) for c in top3))


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=9)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
