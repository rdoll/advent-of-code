#!/usr/bin/python3

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 02 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args

def search_range(start: int, end: int) -> int:
    invalid_count: int = 0
    invalid_total: int = 0

    for product_id in range(start, end + 1):
        product_id_str: str = str(product_id)
        half: int = len(product_id_str) // 2
        for size in range(half, 0, -1):
            if len(product_id_str) % size == 0:  # only process multiples of size
                groups: list[str] = re.compile(r'(.{' + str(size) + r'})').findall(product_id_str)
                if len(groups) != len(product_id_str) // size:
                    break  # skip if it wasn't a complete match

                all_match = True
                for group in groups[1:]:
                    if group != groups[0]:
                        all_match = False
                        break
                if all_match:
                    invalid_count += 1
                    invalid_total += product_id
                    logging.debug(f'Matched {product_id=}')
                    break

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
