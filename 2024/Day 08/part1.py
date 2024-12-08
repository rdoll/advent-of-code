#!/usr/bin/python3

#
# Advent of Code 2024 Day 08 Part One
#

import argparse
import logging
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 08 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class AntennaGroup:
    def __init__(self, symbol: str, pos: tuple[int, int] = None):
        self.symbol = symbol
        self.nodes = []
        self.antinodes = set()
        if pos:
            self.add(symbol, pos)

    def __str__(self):
        return f'symbol={self.symbol}, nodes={self.nodes}, antinodes={self.antinodes}'

    def add(self, symbol: str, pos: tuple[int, int]):
        assert self.symbol == symbol, f'Symbol {symbol} must match group {self}'
        assert pos not in self.nodes, f'Already have {symbol} at {pos} in group {self}'
        self.nodes.append(pos)

    def find_antinodes(self, rows: int, columns: int):
        assert len(self.antinodes) == 0, f'Already have antinodes {self}'
        if len(self.nodes) < 2:
            logging.info(f'No antinodes possible for {self}')
            return

        for i1 in range(0, len(self.nodes) - 1):
            [r1, c1] = self.nodes[i1]
            for i2 in range(i1 + 1, len(self.nodes)):
                [r2, c2] = self.nodes[i2]
                delta_row = r1 - r2
                delta_col = c1 - c2

                behind_n1 = (r1 + delta_row, c1 + delta_col)
                if behind_n1[0] in range(0, rows) and behind_n1[1] in range(0, columns):
                    self.antinodes.add(behind_n1)

                behind_n2 = (r2 - delta_row, c2 - delta_col)
                if behind_n2[0] in range(0, rows) and behind_n2[1] in range(0, columns):
                    self.antinodes.add(behind_n2)

        logging.debug(f'Found antinodes {self}')


class Map:
    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.antenna_groups = {}

    def __str__(self):
        return f'size=({self.rows},{self.columns}), len(antenna_groups)={len(self.antenna_groups)}'

    def print(self, level=logging.DEBUG, include_antenna: bool = False):
        grid: list[list[str]] = []
        for r in range(0, self.rows):
            grid.append(["." for c in range(0, self.columns)])

        for ag in self.antenna_groups.values():
            for n in ag.nodes:
                grid[n[0]][n[1]] = ag.symbol

        for r in range(0, self.rows):
            logging.log(level=level, msg=f'  {"".join(grid[r])}')

        if include_antenna:
            for sym in sorted(self.antenna_groups.keys()):
                logging.log(level=level, msg=self.antenna_groups[sym])

    def add_antenna(self, symbol: str, pos: tuple[int, int]):
        if symbol in self.antenna_groups:
            self.antenna_groups[symbol].add(symbol, pos)
        else:
            self.antenna_groups[symbol] = AntennaGroup(symbol, pos)

    def find_antinodes(self):
        for sym in sorted(self.antenna_groups.keys()):
            self.antenna_groups[sym].find_antinodes(self.rows, self.columns)


def load_map(input_file) -> Map:
    map: Map = Map()
    for line in input_file:
        line = line.strip()
        if not line:
            continue

        map.rows += 1
        row = list(line)
        if map.columns > 0:
            if len(row) != map.columns:
                raise RuntimeError(f'In row {map.rows}, number of columns changed from {map.columns} to {len(row)}')
        else:
            map.columns = len(row)

        for c in range(0, map.columns):
            if row[c] != ".":
                map.add_antenna(row[c], (map.rows - 1, c))

    logging.info(f'Loaded map {map}')
    map.print(level=logging.INFO, include_antenna=True)
    return map


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    map = load_map(args.input_file[0])
    map.find_antinodes()
    antinodes: set[tuple[int, int]] = set()
    for ag in map.antenna_groups.values():
        for an in ag.antinodes:
            antinodes.add(an)
    logging.debug(f'unique antinodes at {antinodes}')
    logging.info(f'Found {len(antinodes)} antinodes in map')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
