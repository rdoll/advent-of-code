#!/usr/bin/python3

import argparse
import logging
import re
import sys
from io import TextIOWrapper
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 05 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def make_nonoverlapping_ranges(range1: range, range2: range) -> range | None:
    # If one range is entirely less than the other, they don't overlap
    if range1.stop - 1 < range2.start or range2.stop - 1 < range1.start:
        return None

    # They overlap from lowest start to highest stop
    return range(
        range1.start if range1.start <= range2.start else range2.start,
        range1.stop if range1.stop >= range2.stop else range2.stop)


def reduce_product_ranges(product_ranges: List[range]) -> List[range]:
    reduced_ranges: List[range] = []
    unreduced_ranges: List[range] = list(product_ranges)

    while len(unreduced_ranges) > 0:
        reduced: range = unreduced_ranges.pop(0)
        for checking in list(unreduced_ranges):
            overlap: range | None = make_nonoverlapping_ranges(reduced, checking)
            if overlap is not None:
                reduced = overlap
                unreduced_ranges.remove(checking)
        reduced_ranges.append(reduced)

    return reduced_ranges


def read_product_ranges(input_file: TextIOWrapper) -> List[range]:
    product_ranges: List[range] = []
    for line in input_file:
        match = re.match(r'^\s*(\d+)-(\d+)\s*$', line.strip())
        if not match:
            break
        product_range: range = range(int(match.group(1)), int(match.group(2)) + 1)
        product_ranges.append(product_range)
    return product_ranges


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    fresh_product_ranges: List[range] = read_product_ranges(args.input_file[0])
    logging.info(f'Read {len(fresh_product_ranges)} fresh product ranges')

    # Crudely repeat reduction once for each range we read -- it can't be more than that
    nonoverlapping_ranges: List[range] = fresh_product_ranges
    for i in range(0, len(fresh_product_ranges)):
        nonoverlapping_ranges = reduce_product_ranges(nonoverlapping_ranges)
    logging.info(f'Reduced to {len(nonoverlapping_ranges)} nonoverlapping ranges')

    all_fresh_count: int = 0
    for fresh_product_range in nonoverlapping_ranges:
        all_fresh_count += len(fresh_product_range)
    logging.info(f'Final {all_fresh_count=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
