import statistics
from typing import List

from aocd.models import Puzzle

chunk_pairs = {
    '[': ']',
    '(': ')',
    '{': '}',
    '<': '>',
}


def part1(input_data: str) -> int:
    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }
    total_points = 0
    for line in input_data.splitlines():
        stack: List[str] = []
        for symbol in line:
            if symbol in chunk_pairs:
                stack.append(chunk_pairs[symbol])
                continue
            if not stack:  # Line has extra close symbols
                break
            expected = stack.pop()
            if symbol != expected:  # Line is corrupt
                total_points += points[symbol]
    return total_points


def part2(input_data: str) -> int:
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }
    line_points: List[int] = []
    for line in input_data.splitlines():
        stack: List[str] = []
        for symbol in line:
            if symbol in chunk_pairs:
                stack.append(chunk_pairs[symbol])
                continue
            if not stack:  # Line has extra close symbols
                break
            expected = stack.pop()
            if symbol != expected:  # Line is corrupt
                break
        else:
            total_points = 0
            while stack:  # Line is incomplete.
                total_points = (total_points * 5) + points[stack.pop()]
            line_points.append(total_points)
    return int(statistics.median(line_points))


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=10)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
