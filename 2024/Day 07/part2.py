#!/usr/bin/python3

#
# Advent of Code 2024 Day 07 Part Two
#

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 07 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-m', '--max-lines', metavar='#', type=int, default=0,
                        help='constrain input to this many lines, 0 = disabled')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Calibration:
    def __init__(self, total: int, operands: list[int]):
        self.total = total
        self.operands = operands

    def __str__(self):
        return f'total={self.total}, operands={self.operands}'

    def try_next_operand(self, subtotal: int, operands: list[int]) -> bool:
        # if no more operands, compare subtotal to total
        if len(operands) == 0:
            return subtotal == self.total

        operand = operands[0]

        # try add
        test_subtotal: int = subtotal + operand
        valid: bool = self.try_next_operand(test_subtotal, operands[1:])
        if valid:
            return True

        # try mult
        test_subtotal = subtotal * operand
        valid = self.try_next_operand(test_subtotal, operands[1:])
        if valid:
            return True

        # try concat
        test_subtotal = int(str(subtotal) + str(operand))
        return self.try_next_operand(test_subtotal, operands[1:])


    def can_be_valid(self) -> bool:
        if len(self.operands) == 1:
            logging.info(f'Calibration with 1 operand: {self}')
            return self.total == self.operands[0]

        return self.try_next_operand(self.operands[0], self.operands[1:])


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    lines: int = 0
    sum: int = 0
    valid_count: int = 0
    for line in args.input_file[0]:
        lines += 1
        line = line.strip()
        if not line:
            continue

        total = re.findall(r'^(\d+):', line)
        operands = re.findall(r' (\d+)', line)
        calibration = Calibration(int(total[0]), [int(o) for o in operands])
        logging.debug(f'Calibration {calibration}')
        if calibration.can_be_valid():
            logging.info(f'Calibration {calibration} can be valid')
            valid_count += 1
            sum += calibration.total
        else:
            logging.debug(f'Calibration {calibration} is invalid')

        if args.max_lines > 0 and lines >= args.max_lines:
            logging.warning(f'Halting load after {lines} of input per max lines {args.max_lines}')
            break
    logging.info(f'Found {valid_count} in {lines} input lines that totalled {sum}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
