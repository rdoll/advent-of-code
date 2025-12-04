#!/usr/bin/python3

import argparse
import logging
import re
import sys
from typing import Tuple, List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 04 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Grid:
    ROLL: str = '@'
    ADJACENT_OFFSETS: List[Tuple[int, int]] = [
        (-1, -1), (-1, 0), (-1, +1),
        ( 0, -1),          ( 0, +1),
        (+1, -1), (+1, 0), (+1, +1),
    ]
    rows: List[str]

    def __init__(self):
        self.rows = []

    def width(self) -> int:
        return 0 if len(self.rows) == 0 else len(self.rows[0])

    def height(self) -> int:
        return len(self.rows)

    def add_row(self, row: str) -> None:
        if 0 < self.width() != len(row):
            raise ValueError(f'row length {len(row)} does not match width {self.width()}')
        self.rows.append(row)

    def has_roll(self, position: Tuple[int, int]) -> bool:
        (row, col) = position
        if row < 0 or row > self.height() - 1:
            return False
        if col < 0 or col > self.width() - 1:
            return False
        return self.rows[row][col] == self.ROLL

    def is_accessible(self, position: Tuple[int, int]) -> bool:
        (row, col) = position
        adjacent_rolls: int = 0
        for offset in self.ADJACENT_OFFSETS:
            offset_position = (row + offset[0], col + offset[1])
            if self.has_roll(offset_position):
                adjacent_rolls += 1
        return True if adjacent_rolls < 4 else False


def find_accessible_rolls(grid: Grid) -> int:
    accessible: int = 0
    for row in range(grid.height()):
        for col in range(grid.width()):
            if grid.has_roll((row, col)):
                if grid.is_accessible((row, col)):
                    accessible += 1
        logging.debug(f'After {row=} {accessible=}')
    return accessible


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    grid = Grid()
    valid_input_pattern = re.compile(r'^\s*([.@]+)\s*$')
    for line in args.input_file[0]:
        match = valid_input_pattern.match(line.strip())
        if match:
            grid.add_row(match.group(1))
        else:
            logging.info(f'Skipping invalid {line=}')
    total: int = find_accessible_rolls(grid)
    logging.info(f'Final {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
