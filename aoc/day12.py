from typing import List, Callable

from aocd.models import Puzzle
from networkx import from_edgelist, Graph


def parse(input_data) -> Graph:
    return from_edgelist(line.split('-') for line in input_data.splitlines())


def is_large_cave(name: str) -> bool:
    return all(c.isupper() for c in name)


def count_paths_to_end(start: str, g: Graph, visited: List[str],
                       can_visit: Callable[[str, List[str]], bool]) -> int:
    visited = visited + [start]
    if start == 'end':
        return 1
    n_paths_to_end = 0
    for neighbour in g.neighbors(start):
        if can_visit(neighbour, visited):
            n_paths_to_end += count_paths_to_end(neighbour, g, visited,
                                                 can_visit)
    return n_paths_to_end


def can_visit_part1(n: str, visited: List[str]) -> bool:
    return is_large_cave(n) or n not in visited


def can_visit_part2(n: str, visited: List[str]) -> bool:
    if n == 'start':
        return False
    if is_large_cave(n):
        return True
    if n not in visited:
        return True
    small_caves = [c for c in visited if not is_large_cave(c)]
    small_caves_visited_once = len(small_caves) == len(set(small_caves))
    return small_caves_visited_once


def part1(input_data: str) -> int:
    g = parse(input_data)
    return count_paths_to_end('start',
                              g,
                              visited=[],
                              can_visit=can_visit_part1)


def part2(input_data: str) -> int:
    g = parse(input_data)
    return count_paths_to_end('start',
                              g,
                              visited=[],
                              can_visit=can_visit_part2)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=12)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
