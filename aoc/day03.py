from aocd.models import Puzzle


def part1(input_data: str) -> int:
    lines = input_data.splitlines()
    column_sums = [0] * len(lines[0])
    for line in lines:
        bits = [int(bit) for bit in line]
        column_sums = [(a + b) for (a, b) in zip(column_sums, bits)]
    gamma_rate = ''.join('1' if count > (len(lines) / 2) else '0'
                         for count in column_sums)
    epsilon_rate = ''.join('0' if bit == '1' else '1' for bit in gamma_rate)
    return int(gamma_rate, 2) * int(epsilon_rate, 2)


def part2(input_data: str):
    pass


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=3)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
