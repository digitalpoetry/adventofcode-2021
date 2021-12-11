from dataclasses import dataclass, field
from typing import List

from aocd.models import Puzzle
"""
1 is the only digit that uses 2 segments
7 is the only digit that uses 3 segments
4 is the only digit that uses 4 segments
8 is the only digit that uses all 7 segments
"""


@dataclass
class NoteEntry:
    signal_patterns: List[str]
    outputs: List[str]

    @staticmethod
    def from_string(s: str) -> 'NoteEntry':
        sp, o = s.split(' | ')
        return NoteEntry(sp.split(), o.split())


@dataclass
class Notes:
    entries: List[NoteEntry] = field(default_factory=list)


def parse(input_data: str) -> Notes:
    lines = input_data.splitlines()
    notes = Notes()
    for line in lines:
        ne = NoteEntry.from_string(line)
        notes.entries.append(ne)
    return notes


def part1(input_data: str) -> int:
    notes = parse(input_data)
    count = 0
    for entry in notes.entries:
        for o in entry.outputs:
            if len(o) in [2, 3, 4, 7]:
                count += 1
    return count


def part2(input_data: str) -> int:
    _ = parse(input_data)
    raise NotImplementedError


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=8)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
