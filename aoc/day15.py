from typing import Tuple, List

from aocd.models import Puzzle
from networkx import DiGraph, grid_2d_graph
from networkx.algorithms.shortest_paths.generic import shortest_path


def parse(input_data: str) -> Tuple[int, int, DiGraph]:
    lines = input_data.splitlines()
    nrow = len(lines)
    ncol = len(next(iter(lines)))
    g: DiGraph = grid_2d_graph(nrow, ncol, create_using=DiGraph)
    for row, line in enumerate(lines):
        for col, digit in enumerate(line):
            weight = int(digit)
            this: Tuple[int, int] = (row, col)
            that: Tuple[int, int]
            g.nodes.get(this)['risk'] = weight
            for that in g.neighbors(this):
                g.add_edge(this, that, weight=weight)
    return nrow, ncol, g


def col_concat(b1: str, b2: str) -> str:
    if not b1:
        return b2
    lines1 = b1.splitlines()
    lines2 = b2.splitlines()
    assert len(lines1) == len(lines2)
    return '\n'.join(line1 + line2 for line1, line2 in zip(lines1, lines2))


def row_concat(b1: str, b2: str) -> str:
    if not b1:
        return b2
    return b1 + '\n' + b2


def grow_input(input_data: str) -> str:
    template = block_to_grid(input_data)
    larger_block = ""
    for row in range(5):
        row_block = ""
        for col in range(5):
            new = block_to_str(calculate_block(template, row, col))
            row_block = col_concat(row_block, new)
        larger_block = row_concat(larger_block, row_block)
    return larger_block


def block_to_str(block: List[List[int]]) -> str:
    lines: List[str] = []
    for row in block:
        line = ''.join(str(v) for v in row)
        lines.append(line)
    return '\n'.join(lines)


def block_to_grid(block: str) -> List[List[int]]:
    return [[int(v) for v in line] for line in block.splitlines()]


def calculate_block(template: List[List[int]], row: int,
                    col: int) -> List[List[int]]:
    block_result = []
    for r in template:
        row_result = []
        for v in r:
            row_result.append(wrap(v + row + col))
        block_result.append(row_result)
    return block_result


def wrap(risk: int):
    while risk > 9:
        risk -= 9
    return risk


def part1(input_data: str) -> int:
    nrow, ncol, g = parse(input_data)
    start = (0, 0)
    end = (nrow - 1, ncol - 1)
    it = shortest_path(g, start, end, weight='weight')
    path = [g.nodes.get(n)['risk'] for n in it]
    return sum(path[1:])


def part2(input_data: str) -> int:
    input_data = grow_input(input_data)
    return part1(input_data)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=15)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
