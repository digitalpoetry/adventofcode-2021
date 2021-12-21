import itertools
import re
from dataclasses import dataclass
from functools import lru_cache

from aocd.models import Puzzle

board_score = [10, 1, 2, 3, 4, 5, 6, 7, 8, 9]
dirac_winning_threshold = 21


@dataclass
class DeterministicDie:
    generator = ((i % 100) + 1 for i in itertools.count())
    roll_tally = 0

    def roll(self) -> int:
        self.roll_tally += 1
        return next(self.generator)


def add_elements(t1, t2: tuple) -> tuple:
    return tuple(sum(x) for x in zip(t1, t2, strict=True))  # type: ignore


@lru_cache(maxsize=1_000_000_000)
def dirac(player_position, player_score, turn=0) -> tuple:
    assert not any(score >= dirac_winning_threshold for score in player_score)

    current_player = turn % len(player_position)
    current_position = player_position[current_player]
    current_score = player_score[current_player]

    player_wins = (0, ) * len(player_position)
    for roll_result in itertools.product((1, 2, 3), repeat=3):
        move = sum(roll_result)
        new_position = (current_position + move) % len(board_score)
        new_score = current_score + board_score[new_position]

        if new_score >= dirac_winning_threshold:
            player_wins = add_elements(
                player_wins,
                tuple(1 if i == current_player else 0
                      for i in range(len(player_position))))
        else:
            positions = list(player_position)
            positions[current_player] = new_position
            scores = list(player_score)
            scores[current_player] += board_score[new_position]
            player_wins = add_elements(
                player_wins, dirac(tuple(positions), tuple(scores), turn + 1))

    return player_wins


def parse(input_data):
    _, p1_start, _, p2_start = map(int, re.findall(r'\d+', input_data))
    return p1_start, p2_start


def part1(input_data: str) -> int:
    die = DeterministicDie()
    player_position = list(parse(input_data))
    player_score = [0] * len(player_position)
    turn = 0
    while not any(score >= 1000 for score in player_score):
        current_player = turn % len(player_position)
        current_position = player_position[current_player]

        move = die.roll() + die.roll() + die.roll()
        new_position = (current_position + move) % len(board_score)

        player_score[current_player] += board_score[new_position]
        player_position[current_player] = new_position
        turn += 1
    return min(player_score) * die.roll_tally


def part2(input_data: str) -> int:
    player_position = tuple(parse(input_data))
    player_score = (0, ) * len(player_position)
    wins = dirac(player_position, player_score)
    return max(wins)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=21)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
