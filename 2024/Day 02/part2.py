#!/usr/bin/python3

#
# Advent of Code 2024 Day 02 Part Two
#

import argparse
import logging
import sys
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 02 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-m', '--max-lines', metavar='#', type=int, default=0,
                        help='constrain input to this many lines, 0 = disabled')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def is_safe_between(vals: List[int], min: int, max: int) -> bool:
    prev = vals[0]
    rest = vals[1:]
    while len(rest) > 0:
        next = rest.pop(0)
        if not next - prev in range(min, max + 1):
            return False
        prev = next
    return True


def is_safe(vals: List[int]) -> bool:
    if len(vals) < 2:
        return False
    if is_safe_between(vals, 1, 3) or is_safe_between(vals, -3, -1):
        logging.debug(f'vals={vals} safe with nothing removed')
        return True

    if len(vals) < 3:
        return False
    for i in range(0, len(vals)):
        vals_without_one = vals.copy()
        removed = vals_without_one.pop(i)
        if is_safe_between(vals_without_one, 1, 3) or is_safe_between(vals_without_one, -3, -1):
            logging.debug(f'vals={vals_without_one} safe with {removed} removed')
            return True
        else:
            logging.debug(f'vals={vals_without_one} unsafe with {removed} removed')
    logging.debug(f'*** vals={vals} unsafe ***')
    return False


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    lines = 0
    safe = 0
    for line in args.input_file[0]:
        lines += 1
        vals = [int(v) for v in line.split()]
        if is_safe(vals):
            safe += 1
        if args.max_lines > 0 and lines >= args.max_lines:
            logging.warning(f'Halting after {lines} of input per max lines {args.max_lines}')
            break
    logging.info(f'Found {safe} reports out of {lines} total reports')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
