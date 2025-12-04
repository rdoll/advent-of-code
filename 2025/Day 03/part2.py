#!/usr/bin/python3

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 03 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def find_joltage(battery_bank: str) -> int:
    joltage_indexes: list[int] = []

    for digit_position in range(12, 0, -1):
        highest_digit_index: int = -1
        for digit in range(9, -1, -1):
            start_index: int = joltage_indexes[len(joltage_indexes) - 1] + 1 if len(joltage_indexes) > 0 else 0
            end_index: int = len(battery_bank) - (digit_position - 1)
            index: int = battery_bank.find(str(digit), start_index, end_index)
            if index != -1:
                highest_digit_index = index
                break
        if highest_digit_index == -1:
            raise IndexError(f'{battery_bank=} {joltage_indexes=}')
        joltage_indexes.append(highest_digit_index)

    joltage: str = ''
    for joltage_index in joltage_indexes:
        joltage += battery_bank[joltage_index]
    logging.info(f'{joltage=} {battery_bank=}')
    return int(joltage)


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    total: int = 0
    valid_input_pattern = re.compile(r'^\s*(\d{12,})\s*$')
    for line in args.input_file[0]:
        match = valid_input_pattern.match(line.strip())
        if match:
            total += find_joltage(match[0])
        else:
            logging.warning(f'Skipping invalid {line=}')
    logging.info(f'Final {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
