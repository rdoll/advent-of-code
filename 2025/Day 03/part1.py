#!/usr/bin/python3

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 03 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def find_joltage(battery_bank: str) -> int:
    tens_digit_index: int = -1
    for tens_digit in range(9, -1, -1):
        index: int = battery_bank.find(str(tens_digit))
        if index != -1 and index + 1 < len(battery_bank):
            tens_digit_index = index
            break

    ones_digit_index: int = -1
    for ones_digit in range(9, -1, -1):
        index: int = battery_bank.find(str(ones_digit), tens_digit_index + 1)
        if index != -1:
            ones_digit_index = index
            break

    joltage: int = int(battery_bank[tens_digit_index]) * 10 + int(battery_bank[ones_digit_index])
    logging.info(f'Joltage {joltage=} {battery_bank=}')
    return joltage


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    total: int = 0
    valid_input_pattern = re.compile(r'^\s*(\d+)\s*$')
    for line in args.input_file[0]:
        match = valid_input_pattern.match(line.strip())
        if match:
            total += find_joltage(match[0])
        else:
            logging.info(f'Skipping invalid {line=}')
    logging.info(f'Final {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
