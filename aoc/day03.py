from functools import reduce
from typing import List

from aocd.models import Puzzle


def part1(input_data: str) -> int:
    lines = input_data.splitlines()
    column = columnar_sum(lines)
    gamma_rate = ''.join('1' if count >= (len(lines) / 2) else '0'
                         for count in column)
    epsilon_rate = ''.join('0' if bit == '1' else '1' for bit in gamma_rate)
    return multiply_bin(gamma_rate, epsilon_rate)


def columnar_sum(lines: List[str]) -> List[int]:
    column_sums = [0] * len(lines[0])
    for line in lines:
        bits = [int(bit) for bit in line]
        column_sums = [(a + b) for (a, b) in zip(column_sums, bits)]
    return column_sums


def multiply_bin(*binary: str) -> int:
    return reduce(lambda x, y: x * y, (int(b, 2) for b in binary))


def part2(input_data: str) -> int:
    lines = input_data.splitlines()
    word_size = len(lines[0])

    sample = list(lines)
    for col in range(word_size):
        count = columnar_sum([line[col] for line in sample])[0]
        ones_most_common = count >= len(sample) / 2
        sample = [
            line for line in sample if line[col] == str(int(ones_most_common))
        ]
        if len(sample) == 1:
            break
    oxygen_generator_rating = sample[0]

    sample = list(lines)
    for col in range(word_size):
        count = columnar_sum([line[col] for line in sample])[0]
        ones_most_common = count >= len(sample) / 2
        sample = [
            line for line in sample
            if line[col] == ('0' if ones_most_common else '1')
        ]
        if len(sample) == 1:
            break
    co2_scrubber_rating = sample[0]

    return multiply_bin(oxygen_generator_rating, co2_scrubber_rating)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=3)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
