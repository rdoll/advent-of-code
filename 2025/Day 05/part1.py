#!/usr/bin/python3

import argparse
import logging
import re
import sys
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 05 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def read_fresh_products(input_file) -> List[range]:
    fresh_products: List[range] = []
    for line in input_file:
        match = re.match(r'^\s*(\d+)-(\d+)$', line.strip())
        if not match:
            break
        fresh_products.append(range(int(match.group(1)), int(match.group(2)) + 1))
    return fresh_products


def is_product_fresh(product_id: int, fresh_products: List[range]) -> bool:
    for fresh_range in fresh_products:
        if product_id in fresh_range:
            return True
    return False


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    fresh_products: List[range] = read_fresh_products(args.input_file[0])
    logging.info(f'Read {len(fresh_products)} fresh product ranges')

    fresh_count: int = 0
    for line in args.input_file[0]:
        match = re.match(r'^\s*(\d+)\s*$', line.strip())
        if match:
            product_id = int(match.group(1))
            if is_product_fresh(product_id, fresh_products):
                fresh_count += 1
                logging.debug(f'{product_id=} is fresh')
            else:
                logging.debug(f'{product_id=} is not fresh')
        else:
            logging.warning(f'Skipping invalid product ID {line=}')
    logging.info(f'Final {fresh_count=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
