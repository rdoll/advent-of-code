#!/usr/bin/python3

import argparse
import logging
import sys
from io import TextIOWrapper
from typing import List, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 07 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Teleporter:
    EMPTY: str = '.'
    START: str = 'S'
    SPLITTER: str = '^'
    BEAM: str = '|'
    COMMENT: str = ';'
    grid: List[str]

    def __init__(self):
        self.grid = []

    def read_input(self, input_file: TextIOWrapper) -> None:
        for raw_line in input_file:
            line: str = raw_line.strip()
            if line[0] == self.COMMENT:
                logging.warning(f'Skipping {raw_line=}')
            else:
                self.grid.append(line)
        logging.info(f'rows={len(self.grid)}, cols={len(self.grid[0])}')

    def dump(self, level: int) -> None:
        for line in self.grid:
            logging.log(level, line)

    def start_col(self) -> int:
        return self.grid[0].index(self.START)

    def spawn_beam(self, row, col) -> List[Tuple[int, int]]:
        splits: List[Tuple[int, int]] = []

        while row < len(self.grid):
            cell: str = self.grid[row][col]
            if cell == self.START and row == 0:
                row += 1
                pass
            elif cell == self.BEAM:
                break
            elif cell == self.EMPTY:
                self.grid[row] = self.grid[row][0:col] + self.BEAM + self.grid[row][col+1:]
                row += 1
                pass
            elif cell == self.SPLITTER:
                splits.append((row, col))
                if col - 1 >= 0:
                    for s in self.spawn_beam(row, col - 1):
                        splits.append(s)
                if col + 1 < len(self.grid[0]):
                    for s in self.spawn_beam(row, col + 1):
                        splits.append(s)
                break
            else:
                raise ValueError(f'Unknown {cell=} at {row=}, {col=}')

        logging.debug(f'spawned beam {row=}, {col=}, {splits=}')
        self.dump(logging.DEBUG)
        return splits


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    teleporter = Teleporter()
    teleporter.read_input(args.input_file[0])
    teleporter.dump(logging.DEBUG)

    beam_splits: List[Tuple[int, int]] = teleporter.spawn_beam(0, teleporter.start_col())
    teleporter.dump(logging.INFO)
    logging.info(f'Final {len(beam_splits)=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
