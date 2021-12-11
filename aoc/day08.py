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
    notes = parse(input_data)
    total = 0
    for entry in notes.entries:
        patterns = [set(sp) for sp in entry.signal_patterns]
        outputs = [set(o) for o in entry.outputs]

        # Length-unique digits can be identified immediately
        one = next((p for p in patterns if len(p) == 2))
        seven = next((p for p in patterns if len(p) == 3))
        four = next((p for p in patterns if len(p) == 4))
        eight = next((p for p in patterns if len(p) == 7))

        decoded: List[str] = []
        for o in outputs:
            if o == one:
                decoded.append('1')
            elif o == seven:
                decoded.append('7')
            elif o == four:
                decoded.append('4')
            elif o == eight:
                decoded.append('8')
            elif len(o) == 5 and len(o & four) == 2:
                decoded.append('2')
            elif len(o) == 5 and len(o & seven) == 3:
                decoded.append('3')
            elif len(o) == 5 and len(o & four) == 3 and len(o & one) == 1:
                decoded.append('5')
            elif len(o) == 6 and len(o & four) == 4:
                decoded.append('9')
            elif len(o) == 6 and len(o & four) == 3 and len(o & one) == 1:
                decoded.append('6')
            elif len(o) == 6 and len(o & four) == 3 and len(o & one) == 2:
                decoded.append('0')
            else:
                raise ValueError('Unable to decode signal pattern to digit.')
        total += int(''.join(decoded))

    return total


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=8)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
