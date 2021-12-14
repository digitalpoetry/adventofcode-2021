import itertools
from collections import Counter
from typing import Dict, Tuple

from aocd.models import Puzzle


def parse(input_data) -> Tuple[str, Dict[str, str]]:
    it = iter(input_data.splitlines())
    template = next(it)
    next(it)  # Consume empty line
    rules: Dict[str, str] = {}
    for rule in it:
        left, right = rule.split(' -> ')
        rules[left] = right
    return template, rules


def polymerise(digraphs: Counter[str], rules: Dict[str, str]):
    new_digraphs: Counter[str] = Counter()
    for d, count in digraphs.items():
        middle = rules[d]
        new_digraphs[d[0] + middle] += count
        new_digraphs[middle + d[1]] += count
    return new_digraphs


def digraph_counter_to_monomer_counter(digraphs: Counter[str]) -> Counter[str]:
    double_counts: Counter[str] = Counter()
    for d, count in digraphs.items():
        double_counts[d[0]] += count
        double_counts[d[1]] += count
    monomers: Counter[str] = Counter()
    for m, count in double_counts.items():
        monomers[m] = (count + 1) // 2
    return monomers


def part1(input_data: str) -> int:
    template, rules = parse(input_data)
    digraphs = Counter(''.join(pair) for pair in itertools.pairwise(template))
    for _ in range(10):
        digraphs = polymerise(digraphs, rules)
    monomers = digraph_counter_to_monomer_counter(digraphs)
    counts = monomers.most_common()
    return counts[0][1] - counts[-1][1]


def part2(input_data: str) -> int:
    template, rules = parse(input_data)
    digraphs = Counter(''.join(pair) for pair in itertools.pairwise(template))
    for _ in range(40):
        digraphs = polymerise(digraphs, rules)
    monomers = digraph_counter_to_monomer_counter(digraphs)
    counts = monomers.most_common()
    return counts[0][1] - counts[-1][1]


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=14)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
