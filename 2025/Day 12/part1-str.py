#!/usr/bin/python3

import argparse
import copy
import logging
import re
import sys
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 12 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Shape:
    FILLED: str = '#'
    EMPTY: str = '.'
    WIDTH: int = 3
    HEIGHT: int = 3
    index: int = 0
    rows: List[List[str]]

    def __init__(self, index: int) -> None:
        self.index = index
        self.rows = [[]]

    def __repr__(self) -> str:
        return f'Shape({self.index}, {self.rows})'

    def __str__(self) -> str:
        return f'{self.index}=' + '\n'.join(self.rows[0])

    def add_row(self, row: str) -> None:
        assert len(row) == self.WIDTH
        self.rows[0].append(row)
        assert len(self.rows) <= self.HEIGHT

    @staticmethod
    def _rotate_90(rows: List[str]) -> List[str]:
        assert Shape.WIDTH == 3 and Shape.HEIGHT == 3   # rotation algorithm only support 3x3
        new_rows: List[str] = [
            rows[2][0] + rows[1][0] + rows[0][0],
            rows[2][1] + rows[1][1] + rows[0][1],
            rows[2][2] + rows[1][2] + rows[0][2]]
        return new_rows

    def completed(self) -> None:
        assert len(self.rows) == 1
        assert len(self.rows[0]) == self.HEIGHT
        for row in self.rows[0]:
            assert len(row) == self.WIDTH
        for r in range(1, 4):
             self.rows.append(Shape._rotate_90(self.rows[r - 1]))

    def rotation(self, rot: int) -> List[str]:
        return self.rows[rot]


class Region:
    width: int
    height: int
    shape_counts: List[int]

    def __init__(self, width: int, height: int, shape_counts: List[int]) -> None:
        self.width = width
        self.height = height
        self.shape_counts = shape_counts

    def __str__(self) -> str:
        return f'Region({self.width}x{self.height}, {self.shape_counts})'


class Grid:
    region: Region
    shapes: List[Shape]
    grid: List[str]
    shape_counts: List[int]

    def __init__(self,
                 region: Region,
                 shapes: List[Shape],
                 grid: List[str] | None = None,
                 shape_counts: List[int] | None = None) -> None:
        self.region = region
        self.shapes = shapes
        if grid is None:
            self.grid = [Shape.EMPTY * region.width for _ in range(region.height)]
        else:
            self.grid = [str(row) for row in grid]
        if shape_counts is None:
            self.shape_counts = [0] * len(shapes)
        else:
            self.shape_counts = list(shape_counts)

    def __copy__(self) -> 'Grid':
        return type(self)(self.region, self.shapes, self.grid, self.shape_counts)

    def place_shape_at(self, row: int, col: int, index: int, rotation: List[str]) -> bool:
        for r in range(Shape.HEIGHT):
            merged: str = ''
            for c in range(Shape.WIDTH):
                grid_char: str = self.grid[row + r][col + c]
                rot_char: str = rotation[r][c]
                if grid_char == Shape.FILLED:
                    if rot_char == Shape.FILLED:
                        return False
                    else:
                        merged += grid_char
                else:
                    merged += rot_char
            self.grid[row + r] = self.grid[row + r][:col] + merged + self.grid[row + r][col + Shape.WIDTH:]

        self.shape_counts[index] += 1
        assert self.shape_counts[index] <= self.region.shape_counts[index]
        if self.shape_counts == self.region.shape_counts:
            logging.info(f'All shapes matched! {self.shape_counts=}, grid=\n{"\n".join(self.grid)}')
            return True
        return self.place_shapes()

    def place_shape(self, index: int, rotation: List[str]) -> bool:
        for row in range(0, self.region.height - Shape.HEIGHT + 1):
            for col in range(0, self.region.width - Shape.WIDTH + 1):
                # perf opt: most shapes have the center filled, so quick validate on it
                if rotation[1][1] == Shape.FILLED and self.grid[row + 1][col + 1] == Shape.FILLED:
                    continue
                grid: Grid = copy.copy(self)
                if grid.place_shape_at(row, col, index, rotation):
                    return True
        return False

    def place_shapes(self) -> bool:
        for index in range(len(self.shapes)):
            if self.shape_counts[index] + 1 <= self.region.shape_counts[index]:
                for rot in range(0, 4):
                    if self.place_shape(index, self.shapes[index].rotation(rot)):
                        return True
        return False


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    shapes: List[Shape] = []
    regions: List[Region] = []
    for line in args.input_file[0]:
        match: re.Match = re.match(r'^\s*(\d+):\s*$', line.strip())
        if match:
            shape: Shape = Shape(int(match.group(1)))
            for row_num in range(Shape.HEIGHT):
                shape.add_row(args.input_file[0].readline().strip())
            assert args.input_file[0].readline().strip() == ''
            shape.completed()
            logging.debug(f'Read {shape=}')
            shapes.append(shape)
            continue

        match = re.match(r'^\s*(\d+)x(\d+):\s*([0-9 ]+)$', line.strip())
        if not match:
            logging.warning(f'Skipping invalid {line=}')
            continue

        [width, height, shape_counts] = match.groups()
        region: Region = Region(int(width), int(height), [int(c) for c in shape_counts.split()])
        regions.append(region)
    logging.debug(f'Found {len(shapes)=} {len(regions)=}')

    total: int = 0
    for region in regions:
        grid: Grid = Grid(region, shapes)
        if grid.place_shapes():
            total += 1
    logging.info(f'Final total: {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
