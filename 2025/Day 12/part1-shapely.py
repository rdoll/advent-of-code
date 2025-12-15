#!/usr/bin/python3

import argparse
import copy
import logging
import re
import sys
from typing import List, Tuple

import shapely as sly


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
    ROTATE_90_CLOCKWISE: List[Tuple[int, int, int, int]] = [
        (0, 0, 0, 2), (0, 1, 1, 2), (0, 2, 2, 2),
        (1, 0, 0, 1), (1, 1, 1, 1), (1, 2, 2, 1),
        (2, 0, 0, 0), (2, 1, 1, 0), (2, 2, 2, 0)
    ]
    index: int = 0
    multipoints: List[sly.MultiPoint]

    def __init__(self, index: int, rows: List[str]) -> None:
        self.index = index
        self.multipoints = [Shape.to_multipoint(rows)]
        for r in range(1, 4):
            self.multipoints.append(Shape.rotate_90_clockwise(self.multipoints[r - 1]))

    def __repr__(self) -> str:
        return f'Shape({self.index}, {self.multipoints})'

    def __str__(self) -> str:
        return f'{self.index}=' + '\n'.join([str(mp) for mp in self.multipoints])

    @staticmethod
    def to_multipoint(rows: List[str]) -> sly.MultiPoint:
        points: List[sly.Point] = []
        assert len(rows) == Shape.HEIGHT
        for row in range(Shape.HEIGHT):
            assert len(rows[row]) == Shape.WIDTH
            for col in range(Shape.WIDTH):
                if rows[row][col] == Shape.FILLED:
                    points.append(sly.Point(row, col))
        return sly.multipoints(points)

    @staticmethod
    def rotate_90_clockwise(multipoint: sly.MultiPoint) -> sly.MultiPoint:
        rotated_points: List[sly.Point] = []
        for rot_map in Shape.ROTATE_90_CLOCKWISE:
            (current_row, current_col, maps_to_row, maps_to_col) = rot_map
            if multipoint.contains(sly.Point(current_row, current_col)):
                rotated_points.append(sly.Point(maps_to_row, maps_to_col))
        return sly.multipoints(rotated_points)


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
    grid: sly.MultiPoint
    shape_counts: List[int]

    def __init__(self,
                 region: Region,
                 shapes: List[Shape],
                 grid: sly.MultiPoint = None,
                 shape_counts: List[int] | None = None) -> None:
        self.region = region
        self.shapes = shapes
        if grid is None:
            self.grid = sly.MultiPoint()
        else:
            self.grid = sly.MultiPoint(grid)
        if shape_counts is None:
            self.shape_counts = [0] * len(shapes)
        else:
            self.shape_counts = list(shape_counts)

    def __copy__(self) -> 'Grid':
        return type(self)(self.region, self.shapes, self.grid, self.shape_counts)

    def place_shape_at(self, row: int, col: int, index: int, rotation: sly.MultiPoint) -> bool:
        offset_rotation: sly.MultiPoint = sly.MultiPoint([sly.Point(row + p.x, col + p.y) for p in rotation.geoms])
        if self.grid.intersects(offset_rotation):
            return False
        self.grid = self.grid.union(offset_rotation)
        self.shape_counts[index] += 1
        assert self.shape_counts[index] <= self.region.shape_counts[index]
        if self.shape_counts == self.region.shape_counts:
            logging.info(f'All shapes matched! {self.shape_counts=}, {self.grid=}')
            return True
        return self.place_shapes()

    def place_shape(self, index: int, rotation: sly.MultiPoint) -> bool:
        for row in range(0, self.region.height - Shape.HEIGHT + 1):
            for col in range(0, self.region.width - Shape.WIDTH + 1):
                grid: Grid = copy.copy(self)
                if grid.place_shape_at(row, col, index, rotation):
                    return True
        return False

    def place_shapes(self) -> bool:
        for index in range(len(self.shapes)):
            if self.shape_counts[index] + 1 <= self.region.shape_counts[index]:
                for rot in range(0, 4):
                    if self.place_shape(index, self.shapes[index].multipoints[rot]):
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
            index: int = int(match.group(1))
            rows: List[str] = [args.input_file[0].readline().strip() for _ in range(Shape.HEIGHT)]
            assert args.input_file[0].readline().strip() == ''
            shape: Shape = Shape(index, rows)
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
