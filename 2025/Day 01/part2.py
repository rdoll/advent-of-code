#!/usr/bin/python3

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 01 Part 2 Solution')

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

    def turn_broken(self, offset: int) -> int:
        """
        :param offset: positive = right, negative = left
        :return # of times goal position was hit
        """
        if offset == 0:
            raise ValueError("Offset cannot be zero")

        before: int = self.position
        after: int = self.position + offset
        goals: int = 0

        if after == 0:
            goals += 1
        while after > Safe.MAX_POSITION:
            after -= Safe.POSITIONS
            goals += 1
        while after < 0:
            if before != 0 or after < -Safe.MAX_POSITION:
                goals += 1
            after += Safe.POSITIONS

        self.position = after
        logging.debug(f'turn: {before=}, {offset=}, {self.position=}, {goals=}')
        return goals

    def turn(self, offset: int) -> int:
        """
        :param offset: positive = right, negative = left
        :return # of times goal position was hit
        """
        if offset == 0:
            raise ValueError("Offset cannot be zero")

        before: int = self.position
        after: int = self.position
        steps: int = abs(offset)
        goals: int = 0

        while steps > 0:
            steps -= 1
            if offset > 0:
                if after == Safe.MAX_POSITION:
                    goals += 1
                    after = Safe.MIN_POSITION
                else:
                    after += 1
            elif offset < 0:
                if after == Safe.MIN_POSITION:
                    after = Safe.MAX_POSITION
                else:
                    after -= 1
                    if after == Safe.MIN_POSITION:
                        goals += 1

        self.position = after
        logging.debug(f'turn: {before=}, {offset=}, {self.position=}, {goals=}')
        return goals


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    goals: int = 0
    safe: Safe = Safe()
    valid_pattern = re.compile(r'^\s*([LR])(\d+)\s*$')
    for line in args.input_file[0]:
        if valid_pattern.match(line):
            (direction, offset) = valid_pattern.match(line).groups()
            goals += safe.turn(int(offset) if direction == 'R' else -int(offset))
        else:
            logging.info(f'Skipping invalid line {line=}')
    logging.info(f'Final {goals=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
