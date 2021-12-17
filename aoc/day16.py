from dataclasses import dataclass, field
from io import StringIO
from typing import Optional, List, Tuple

from aocd.models import Puzzle
from math import prod


@dataclass
class Packet:
    version: int
    type_id: int
    value: Optional[int]
    children: List['Packet'] = field(default_factory=list)

    def version_sum(self) -> int:
        version = self.version
        for child in self.children:
            version += child.version_sum()
        return version

    def evaluate(self) -> int:
        if self.type_id == 0:
            return sum(child.evaluate() for child in self.children)
        if self.type_id == 1:
            return prod(child.evaluate() for child in self.children)
        if self.type_id == 2:
            return min(child.evaluate() for child in self.children)
        if self.type_id == 3:
            return max(child.evaluate() for child in self.children)
        if self.type_id == 4:
            assert self.value is not None
            return self.value
        if self.type_id == 5:
            return int(
                self.children[0].evaluate() > self.children[1].evaluate())
        if self.type_id == 6:
            return int(
                self.children[0].evaluate() < self.children[1].evaluate())
        if self.type_id == 7:
            return int(
                self.children[0].evaluate() == self.children[1].evaluate())
        raise ValueError(f'Unsupported type id {self.type_id}')

    @staticmethod
    def parse(bits: str) -> Tuple['Packet', str]:
        b = StringIO(bits)
        version = int(b.read(3), 2)
        type_id = int(b.read(3), 2)
        if type_id == 4:
            has_next = True
            nybbles = []
            while has_next:
                has_next = bool(int(b.read(1)))
                nybbles.append(b.read(4))
            return Packet(version, type_id, int(''.join(nybbles), 2)), b.read()
        else:
            children: List[Packet]
            length_type_id = int(b.read(1))
            if length_type_id == 0:
                number_of_bits = int(b.read(15), 2)
                children, remaining_bits = Packet.parse_many(
                    b.read(number_of_bits))
            else:
                number_of_packets = int(b.read(11), 2)
                children, remaining_bits = Packet.parse_many(
                    b.read(), packet_limit=number_of_packets)
                b = StringIO(remaining_bits)
            return Packet(version, type_id, None, children), b.read()

    @staticmethod
    def parse_many(bits: str, packet_limit=-1) -> Tuple[List['Packet'], str]:
        packets: List[Packet] = []
        while bits and packet_limit:
            p, bits = Packet.parse(bits)
            packets.append(p)
            packet_limit -= 1
        return packets, bits


def hex_to_bin(input_data: str):
    table = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111',
    }
    return ''.join(table[c] for c in input_data)


def part1(input_data: str) -> int:
    bits = hex_to_bin(input_data)
    root, _ = Packet.parse(bits)
    return root.version_sum()


def part2(input_data: str) -> int:
    bits = hex_to_bin(input_data)
    root, _ = Packet.parse(bits)
    return root.evaluate()


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=16)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
