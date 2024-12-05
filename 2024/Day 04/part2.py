#!/usr/bin/python3

#
# Advent of Code 2024 Day 04 Part Two
#

import argparse
import logging
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 04 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-m', '--max-lines', metavar='#', type=int, default=0,
                        help='constrain input to this many lines, 0 = disabled')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


WORD_NWSW: list[tuple[str, int, int]] = [("M", -1, -1), ("S",  1,  1), ("M",  1, -1), ("S", -1,  1)]
WORD_NWNE: list[tuple[str, int, int]] = [("M", -1, -1), ("S",  1,  1), ("S",  1, -1), ("M", -1,  1)]
WORD_SESW: list[tuple[str, int, int]] = [("S", -1, -1), ("M",  1,  1), ("M",  1, -1), ("S", -1,  1)]
WORD_SENE: list[tuple[str, int, int]] = [("S", -1, -1), ("M",  1,  1), ("S",  1, -1), ("M", -1,  1)]


def is_word(grid: list[list[str]], start_row: int, start_col: int, word_def: list[tuple[str, int, int]]) -> int:
    rows = len(grid)
    columns = len(grid[0])
    for wd in word_def:
        [letter, row_off, col_off] = wd
        if start_row + row_off not in range(0, rows) or start_col + col_off not in range(0, columns):
            return 0
        if grid[start_row + row_off][start_col + col_off] != letter:
            return 0
    logging.debug(f'Found word at {start_row} x {start_col} for {word_def}')
    return 1


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    rows: int = 0
    columns: int = 0
    grid: list[list[str]] = []
    for line in args.input_file[0]:
        line = line.strip()
        if not line:
            continue

        rows += 1
        row = list(line)
        if columns > 0:
            if len(row) != columns:
                logging.error(f'In row {rows}, number of columns changed from {columns} to {len(row)}')
                return 1
        else:
            columns = len(row)
        grid.append(row)

        if args.max_lines > 0 and rows >= args.max_lines:
            logging.warning(f'Halting after {rows} of input per max lines {args.max_lines}')
            break
    logging.debug(f'Read {rows} x {columns} grid')
    for r in range(0, rows):
        logging.debug(f'  {"".join(grid[r])}')

    words: int = 0
    for r in range(0, rows):
        for c in range(0, columns):
            if grid[r][c] == "A":
                words += is_word(grid, r, c, WORD_NWSW)
                words += is_word(grid, r, c, WORD_NWNE)
                words += is_word(grid, r, c, WORD_SESW)
                words += is_word(grid, r, c, WORD_SENE)
        logging.debug(f'Total words after row {r} is {words}')
    logging.info(f'Found {words} words in the {rows} x {columns} grid')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
