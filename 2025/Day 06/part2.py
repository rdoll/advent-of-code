#!/usr/bin/python3

import argparse
import logging
import re
import sys
from functools import reduce
from io import TextIOWrapper
from typing import List

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 06 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def transpose_input(input_file: TextIOWrapper) -> List[str]:
    input_rows: List[str] = []
    for line in input_file:
        if not re.match(r'^\s*;.*$', line):
            input_rows.append(line.rstrip('\n'))

    max_width = max(len(row) for row in input_rows)
    input_rows = [row.ljust(max_width) for row in input_rows]
    for line in input_rows:
        logging.debug(f'{line=}')

    # '123 328  51 64 '
    # ' 45 64  387 23 '
    # '  6 98  215 314'
    # '*   +   *   +  '

    # left to right into one row
    # '* 1 24 356'
    # '+ 369 248 8'
    # '* 32 581 175'
    # '+ 623 431 4'

    # left to right keeping rows
    # '1   '
    # '24  '
    # '356 '
    # '*   '


    transposed_rows: List[str] = ['' for i in range(len(input_rows[0]) * 2)]  # add padding
    for line in input_rows:
        for i, char in enumerate(line):
            transposed_rows[i] += char
    return [row for row in transposed_rows if row.strip() != '']


def cephalopod_math_total(df: pd.DataFrame, operators: pd.Series) -> int:
    col_totals: List[int] = []
    for col_num in range(0, df.shape[1]):
        col_total: int | None = None
        if operators[col_num] == '+':
            col_total = df.loc[:, col_num].sum()
        elif operators[col_num] == '*':
            col_total = df.loc[:, col_num].prod()
        if col_total is None or col_total < 0:
            raise RuntimeError(f"Column aggregation failed: {col_num=}, {col_total=}, {operators[col_num]=}")
        col_totals.append(col_total)
    logging.info(f"{col_totals=}")

    total: int = reduce(lambda tot, col_tot: tot + col_tot, col_totals, 0)
    return total


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    transposed_input = transpose_input(args.input_file[0])
    for line in transposed_input:
        logging.debug(f'{line=}')

    df = pd.read_table(args.input_file[0], sep=r'\s+', header=None, comment=';')
    (rows, cols) = df.shape
    logging.info(f'Input shape {rows=}, {cols=}')

    operators = df.iloc[rows - 1]
    df.drop(rows - 1, inplace=True)
    logging.debug(f'{operators.tolist()=}')

    total: int = cephalopod_math_total(df.astype(int), operators)
    logging.info(f'Final {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
