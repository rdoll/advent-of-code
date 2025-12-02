#!/usr/bin/python3

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 02 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args

def search_range(start: int, end: int) -> int:
    invalid_count: int = 0
    invalid_total: int = 0

    for id in range(start, end + 1):
        s: str = str(id)
        if len(s) % 2 == 0:  # only even length product IDs can have an exact duplicate
            half: int = len(s) // 2
            (first, second) = s[:half], s[half:]
            if first == second:
                invalid_count += 1
                invalid_total += id
                logging.debug(f'matched {id=}')

    logging.info(f'Range {start}-{end} {invalid_count=} {invalid_total=}')
    return invalid_total

def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    total: int = 0
    range_pattern = re.compile(r'\s*(\d+-\d+),?\s*')
    for line in args.input_file[0]:
        if not range_pattern.match(line):
            logging.info(f'Skipping invalid {line=}')
            continue

        for product_id_range in range_pattern.findall(line):
            (start, end) = product_id_range.split('-')
            total += search_range(int(start), int(end))

    logging.info(f'Final {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
