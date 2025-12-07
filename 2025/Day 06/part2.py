#!/usr/bin/python3

import argparse
import logging
import re
import sys
from functools import reduce
from io import TextIOWrapper
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 06 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def read_grid(input_file: TextIOWrapper) -> List[str]:
    grid: List[str] = []
    for line in input_file:
        if not re.match(r'^\s*;.*$', line):
            grid.append(line.rstrip('\n'))

    max_width = max(len(row) for row in grid)
    grid = [row.ljust(max_width) for row in grid]
    for line in grid:
        logging.debug(f'{line=}')
    logging.info(f'Input grid shape {len(grid)=}, {len(grid[0])=}')
    return grid


def perform_calculation(operands: List[int], operator: str) -> int:
    if operator == '+':
        return reduce(lambda tot, x: tot + x, operands)
    elif operator == '*':
        return reduce(lambda tot, x: tot * x, operands)
    else:
        raise ValueError(f'Unknown {operator=}')


def cephalopod_math_total(grid: List[str]) -> int:
    rows: int = len(grid)
    cols: int = len(grid[0])

    col_totals: List[int] = []

    # '123 328  51 64 '
    # ' 45 64  387 23 '
    # '  6 98  215 314'
    # '*   +   *   +  '

    operands: List[int] = []
    operator: str = ' '
    for col in range(cols - 1, -1, -1):
        line: str = reduce(lambda st, ch: st + ch, [row[col] for row in grid], '')
        if line.strip() == '':
            col_totals.append(perform_calculation(operands, operator))
            operands = []
            operator = ' '
            continue

        op: str = line[rows - 1]
        line = line[:rows - 1]
        operands.append(int(line))
        if op != ' ':
            if operator != ' ':
                raise RuntimeError(f'Duplicate operator: {operator=}, {op=}, {line=}')
            operator = op

    if len(operator) > 0:
        col_totals.append(perform_calculation(operands, operator))

    logging.info(f'{col_totals=}')
    total: int = reduce(lambda tot, col_tot: tot + col_tot, col_totals, 0)
    return total


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    grid: List[str] = read_grid(args.input_file[0])
    total: int = cephalopod_math_total(grid)
    logging.info(f'Final {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
