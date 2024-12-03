#!/usr/bin/python3

#
# Advent of Code 2024 Day 03 Part One
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
    for line in args.input_file[0]:
        lines += 1
        muls: list[tuple[str, str]] = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)
        valid += len(muls)
        for mul in muls:
            sum += int(mul[0]) * int(mul[1])
        logging.debug(f'Found {len(muls)} muls in line {lines}, current total {sum}')

        if args.max_lines > 0 and lines >= args.max_lines:
            logging.warning(f'Halting after {lines} of input per max lines {args.max_lines}')
            break
    logging.info(f'{valid} mul\'s found in {lines} lines of computer memory totalling {sum}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
