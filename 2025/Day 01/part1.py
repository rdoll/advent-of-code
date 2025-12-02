#!/usr/bin/python3

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 01 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args

class Safe:
    START_POSITION = 50
    MIN_POSITION = 0
    MAX_POSITION = 99
    POSITIONS = MAX_POSITION - MIN_POSITION + 1

    position: int

    def __init__(self) -> None:
        self.position = Safe.START_POSITION

    def turn(self, offset: int) -> int:
        """
        :param offset: positive = right, negative = left
        :return new position
        """
        before: int = self.position
        self.position = (self.position + offset) % Safe.POSITIONS
        logging.debug(f'turn: {before=}, {offset=}, {self.position=}')
        return self.position

def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    goal_count: int = 0
    safe: Safe = Safe()
    valid_pattern = re.compile(r'^\s*([LR])(\d+)\s*$')
    for line in args.input_file[0]:
        if valid_pattern.match(line):
            (direction, offset) = valid_pattern.match(line).groups()
            position = safe.turn(int(offset) if direction == 'R' else -int(offset))
            if position == 0:
                goal_count += 1
                logging.info(f'At goal, {goal_count=}')
        else:
            logging.info(f'Skipping invalid line {line=}')
    logging.info(f'Final goal count: {goal_count=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
