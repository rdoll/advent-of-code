#!/usr/bin/python3

#
# Advent of Code 2024 Day 03 Part Two
#

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 03 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-m', '--max-lines', metavar='#', type=int, default=0,
                        help='constrain input to this many lines, 0 = disabled')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    lines: int = 0
    valid: int = 0
    sum: int = 0
    enabled: bool = True
    for line in args.input_file[0]:
        lines += 1
        insts: list[tuple[str, str, str]] = re.findall(
            r"(mul\((\d{1,3}),(\d{1,3})\)|don't\(\)|do\(\))", line)
        valid += len(insts)
        for mul in insts:
            if mul[0] == "do()":
                enabled = True
            elif mul[0] == "don't()":
                enabled = False
            elif enabled:
                sum += int(mul[1]) * int(mul[2])
        logging.debug(f'Found {len(insts)} instructions in line {lines}, current total {sum}')

        if args.max_lines > 0 and lines >= args.max_lines:
            logging.warning(f'Halting after {lines} of input per max lines {args.max_lines}')
            break
    logging.info(f'{valid} instructions found in {lines} of computer memory totalling {sum}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
