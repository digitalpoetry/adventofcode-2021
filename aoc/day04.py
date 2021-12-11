from dataclasses import dataclass
from typing import List, Sequence, Tuple, Union, ClassVar

from aocd.models import Puzzle


@dataclass
class Cell:
    value: int
    isMarked: bool = False


@dataclass
class Board:
    grid: List[Cell]
    SIDE_LENGTH: ClassVar[int] = 5

    @staticmethod
    def from_list(cells: Union[Sequence[int], Sequence[str]]) -> 'Board':
        assert len(cells) == Board.SIDE_LENGTH ** 2, \
            f'must be a list of {Board.SIDE_LENGTH ** 2} cell values.'
        return Board([Cell(int(n)) for n in cells])

    def mark(self, value: int) -> None:
        for cell in self.grid:
            if cell.value == value:
                cell.isMarked = True

    def get_row(self, n: int) -> Sequence[Cell]:
        assert 0 <= n < Board.SIDE_LENGTH, f'must be between [0 and {Board.SIDE_LENGTH}).'
        start, end = Board.SIDE_LENGTH * n, Board.SIDE_LENGTH * (n + 1)
        return self.grid[start:end]

    def get_col(self, n: int) -> Sequence[Cell]:
        assert 0 <= n < Board.SIDE_LENGTH, f'must be between [0 and {Board.SIDE_LENGTH}).'
        seq = [
            self.grid[Board.SIDE_LENGTH * row + n]
            for row in range(Board.SIDE_LENGTH)
        ]
        return seq

    def has_complete_row_or_col(self) -> bool:
        for i in range(Board.SIDE_LENGTH):
            if all(cell.isMarked for cell in self.get_row(i)):
                return True
            if all(cell.isMarked for cell in self.get_col(i)):
                return True
        return False

    def sum_unmarked_cells(self) -> int:
        return sum(cell.value for cell in self.grid if not cell.isMarked)


def parse(input_data: str) -> Tuple[List[int], List[Board]]:
    sequence_input, *boards_input = input_data.split('\n\n')
    sequence = [int(n) for n in sequence_input.split(',')]
    boards = []
    for board_input in boards_input:
        board = Board.from_list(board_input.split())
        boards.append(board)
    return sequence, boards


def part1(input_data: str) -> int:
    sequence, boards = parse(input_data)
    for call in sequence:
        for board in boards:
            board.mark(call)
            if board.has_complete_row_or_col():
                score = board.sum_unmarked_cells() * call
                return score
    raise Exception('No winner')


def part2(input_data: str) -> int:
    sequence, boards = parse(input_data)
    for call in sequence:
        for board in boards:
            board.mark(call)
            if board.has_complete_row_or_col():
                if len(boards) > 1:
                    # Remove this winning board
                    boards = [b for b in boards if b != board]
                else:
                    score = board.sum_unmarked_cells() * call
                    return score
    raise Exception('No winner')


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=4)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
