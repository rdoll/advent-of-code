#!/usr/bin/python3

#
# Advent of Code 2024 Day 01 Part Two
#

import argparse
from collections import Counter
import logging
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 01 Part Two Solution')

    parser.add_argument('--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='Input file')

    args = parser.parse_args()
    return args


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    list1, list2 = [], []
    for line in args.input_file[0]:
        first, second = line.split()
        list1.append(int(first))
        list2.append(int(second))
    logging.info(f'Found {len(list1)} lines in input file')

    logging.debug('Building counter list...')
    counts = Counter(list2)

    sum = 0
    for num in list1:
        sum += num * counts[num] if counts[num] else 0
    logging.info(f'Total similarity score = {sum}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
