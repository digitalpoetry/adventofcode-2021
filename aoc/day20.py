import itertools
from dataclasses import dataclass
from typing import Generator, Any

from aocd.models import Puzzle


@dataclass(frozen=True)
class Coord:
    x: int
    y: int

    def get_box_coordinates(self) -> Generator['Coord', Any, None]:
        for dy, dx in itertools.product((-1, 0, 1), repeat=2):
            yield Coord(self.x + dx, self.y + dy)


@dataclass(frozen=True)
class Image:
    map: dict[Coord, str]

    @staticmethod
    def from_strings(image_data: list[str]) -> 'Image':
        m = {}
        for y, line in enumerate(image_data):
            for x, symbol in enumerate(line):
                m[Coord(x, y)] = symbol
        return Image(m)

    def bounds(self) -> tuple[int, int, int, int]:
        """Top-left inclusive, bottom-right exclusive."""
        min_x = min(c.x for c in self.map.keys())
        min_y = min(c.y for c in self.map.keys())
        max_x = max(c.x for c in self.map.keys()) + 1
        max_y = max(c.y for c in self.map.keys()) + 1
        return min_x, min_y, max_x, max_y

    def extend(self, translate: str, iteration: int) -> 'Image':
        min_x, min_y, max_x, max_y = self.bounds()
        horizon = '.' if iteration % 2 == 0 else translate[0]
        m = {}
        for y in range(min_y - 2, max_y + 2):
            for x in range(min_x - 2, max_x + 2):
                this = Coord(x, y)
                m[this] = self.map.get(this, horizon)
        return Image(m)

    def enhance(self, translate: str) -> 'Image':
        min_x, min_y, max_x, max_y = self.bounds()
        new_lights = {}
        table = str.maketrans('.#', '01')
        for y in range(min_y + 1, max_y - 1):
            for x in range(min_x + 1, max_x - 1):
                centre = Coord(x, y)
                bits = self.get_box(centre).translate(table)
                new_lights[centre] = translate[int(bits, 2)]
        return Image(new_lights)

    def get_box(self, coordinate: Coord) -> str:
        return ''.join(self.map[c] for c in coordinate.get_box_coordinates())

    def count_light_pixels(self) -> int:
        return sum(symbol == '#' for symbol in self.map.values())

    def print(self) -> None:
        min_x, min_y, max_x, max_y = self.bounds()
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                print(self.map[Coord(x, y)], end='')
            print()


def parse(input_data: str) -> tuple[str, Image]:
    translate, image_data = input_data.split('\n\n')
    assert len(translate) == 512
    return translate, Image.from_strings(image_data.split())


def part1(input_data: str) -> int:
    translate, image = parse(input_data)
    for i in range(2):
        image = image.extend(translate, i).enhance(translate)
    return image.count_light_pixels()


def part2(input_data: str) -> int:
    translate, image = parse(input_data)
    for i in range(50):
        image = image.extend(translate, i).enhance(translate)
    return image.count_light_pixels()


if __name__ == '__main__':
    puzzle = Puzzle(year=2021, day=20)
    print(part1(puzzle.input_data))
    print(part2(puzzle.input_data))
