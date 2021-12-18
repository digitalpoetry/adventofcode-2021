import functools
import itertools
from dataclasses import dataclass
from typing import List, Optional, Union

import math
from aocd.models import Puzzle


@dataclass
class SnailFishTerminal:
    value: int = -1
    parent: Optional['SnailFishPair'] = None

    def marshal(self) -> int:
        return self.value

    def magnitude(self) -> int:
        return self.value

    def split(self) -> bool:
        assert self.parent is not None
        if self.value >= 10:
            new = SnailFishPair(SnailFishTerminal(), SnailFishTerminal(),
                                self.parent)
            new.left = SnailFishTerminal(math.floor(self.value / 2),
                                         parent=new)
            new.right = SnailFishTerminal(math.ceil(self.value / 2),
                                          parent=new)
            self.parent.replace_child(self, new)
            return True
        return False

    def explode(self, level=0) -> bool:
        return False

    def is_terminal_pair(self) -> bool:
        return False


@dataclass
class SnailFishPair:
    left: Union['SnailFishPair', SnailFishTerminal]
    right: Union['SnailFishPair', SnailFishTerminal]
    parent: Optional['SnailFishPair']

    @staticmethod
    def from_list(pair: List[Union[int, List]],
                  parent: Optional['SnailFishPair'] = None) -> 'SnailFishPair':
        this = SnailFishPair(SnailFishTerminal(), SnailFishTerminal(), parent)
        if isinstance(pair[0], int):
            this.left = SnailFishTerminal(pair[0], this)
        else:
            this.left = SnailFishPair.from_list(pair[0], this)
        if isinstance(pair[1], int):
            this.right = SnailFishTerminal(pair[1], this)
        else:
            this.right = SnailFishPair.from_list(pair[1], this)
        return this

    @staticmethod
    def add(a, b: 'SnailFishPair') -> 'SnailFishPair':
        a = a.clone()
        b = b.clone()
        root = SnailFishPair(a, b, parent=None)
        a.parent = root
        b.parent = root
        root.reduce()
        return root

    def clone(self) -> 'SnailFishPair':
        return SnailFishPair.from_list(self.marshal())

    def marshal(self) -> List[int | List]:
        return [self.left.marshal(), self.right.marshal()]

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def split(self) -> bool:
        return self.left.split() or self.right.split()

    def explode(self, level=0) -> bool:
        if level == 4:
            assert self.is_terminal_pair()
            prev: Optional[SnailFishTerminal] = self.inorder_prev()
            if prev is not None:
                assert isinstance(self.left, SnailFishTerminal)
                prev.value += self.left.value
            next = self.inorder_next()
            if next is not None:
                assert isinstance(self.right, SnailFishTerminal)
                next.value += self.right.value
            assert self.parent is not None
            self.parent.replace_child(self, SnailFishTerminal(0, self.parent))
            return True
        return self.left.explode(level + 1) or self.right.explode(level + 1)

    def reduce(self) -> None:
        changed = True
        while changed:
            changed = self.explode() or self.split()

    def is_terminal_pair(self):
        return isinstance(self.left, SnailFishTerminal) and isinstance(
            self.right, SnailFishTerminal)

    def inorder_next(self) -> Optional['SnailFishTerminal']:
        assert self.is_terminal_pair(), 'Assumes we are at a terminal pair'
        it: Union[SnailFishPair, SnailFishTerminal] = self
        while it.parent and it.parent.right is it:
            it = it.parent
        if it.parent is None:
            return None
        it = it.parent.right
        while isinstance(it, SnailFishPair):
            it = it.left
        return it

    def inorder_prev(self) -> Optional['SnailFishTerminal']:
        assert self.is_terminal_pair(), 'Assumes we are at a terminal pair'
        it: Union[SnailFishPair, SnailFishTerminal] = self
        while it.parent and it.parent.left is it:
            it = it.parent
        if it.parent is None:
            return None
        it = it.parent.left
        while isinstance(it, SnailFishPair):
            it = it.right
        return it

    def replace_child(
            self, child: Union['SnailFishPair', SnailFishTerminal],
            value: Union['SnailFishPair', SnailFishTerminal]) -> None:
        if self.left == child:
            self.left = value
        elif self.right == child:
            self.right = value
        else:
            raise ValueError('child does not currently exist.')


def parse(input_data: str) -> list[SnailFishPair]:
    lines = input_data.splitlines()
    numbers: List[SnailFishPair] = []
    for line in lines:
        n = SnailFishPair.from_list(eval(line))
        numbers.append(n)
    return numbers


def part1(input_data: str) -> int:
    numbers: List[SnailFishPair] = parse(input_data)
    return functools.reduce(SnailFishPair.add, numbers).magnitude()


def part2(input_data: str) -> int:
    numbers: List[SnailFishPair] = parse(input_data)
    pairs = itertools.permutations(numbers, 2)
    return max(SnailFishPair.add(*pair).magnitude() for pair in pairs)


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=18)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
