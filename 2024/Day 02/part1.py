#!/usr/bin/python3

#
# Advent of Code 2024 Day 02 Part One
#

import argparse
import logging
import sys
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 02 Solution')

    parser.add_argument('--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='Input file')

    args = parser.parse_args()
    return args


def is_safe_between(vals: List[int], min: int, max: int) -> bool:
    prev = vals[0]
    rest = vals[1:]
    while len(rest) > 0:
        next = rest.pop(0)
        if not next - prev in range(min, max + 1):
            logging.debug(f'vals={vals} unsafe for {min}, {max}')
            return False
        prev = next
    logging.debug(f'vals={vals} safe for {min}, {max}')
    return True


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
        if len(vals) >= 2:
            if is_safe_between(vals, 1, 3) or is_safe_between(vals, -3, -1):
                safe += 1
    logging.info(f'Found {safe} reports out of {lines} total reports')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
