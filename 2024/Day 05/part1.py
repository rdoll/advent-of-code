#!/usr/bin/python3

#
# Advent of Code 2024 Day 05 Part One
#

import argparse
import logging
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 05 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-m', '--max-lines', metavar='#', type=int, default=0,
                        help='constrain input to this many lines, 0 = disabled')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def is_valid(update: list[int], rules: dict[int, list[int]]) -> bool:
    prior_pages: list[int] = []
    for page in update:
        if page in rules:
            for must_be_after_page in rules[page]:
                if must_be_after_page in prior_pages:
                    logging.debug(f'Invalid update {update}, {must_be_after_page} must be after {page}')
                    return False
        prior_pages.append(page)
    return True


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    rules: dict[int, list[int]] = {}  # page number in key must be printed before page numbers in value
    updates: list[list[int]] = []
    lines: int = 0
    for line in args.input_file[0]:
        lines += 1
        line = line.strip()
        if not line:
            continue

        if "|" in line:
            [first, second] = [int(n) for n in line.split(sep="|")]
            rules[first] = rules.get(first, []) + [second]

        if "," in line:
            update = [int(n) for n in line.split(",")]
            if len(update) % 2 == 0:
                logging.error(f'Update on line {lines} has an even number of pages {update}!')
                return 1
            updates.append(update)

        if args.max_lines > 0 and lines >= args.max_lines:
            logging.warning(f'Halting after {lines} of input per max lines {args.max_lines}')
            break
    logging.info(f'Found {len(rules)} pages with rules and {len(updates)} updates in {lines} lines of input')

    sum: int = 0
    valid_count: int = 0
    for update in updates:
        if is_valid(update, rules):
            valid_count += 1
            sum += update[len(update) // 2]
    logging.info(f'{valid_count} valid updates totalling {sum} middle page numbers')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
