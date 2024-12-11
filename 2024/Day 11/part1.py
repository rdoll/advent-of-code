#!/usr/bin/python3

#
# Advent of Code 2024 Day 11 Part One
#

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 11 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-b', '--blinks', metavar='#', type=int, default=6,
                        help='blink this many times, 0 = disabled')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    stones: list[int] = []
    for line in args.input_file[0]:
        values = re.findall(r"(\d+)", line)
        assert len(values) > 0, f'No stones in line "{line}"'
        [stones.append(int(v)) for v in values]
    logging.info(f'Stones = {stones}')

    for blink in range(0, args.blinks):
        new_stones: list[int] = []
        for s in range(0, len(stones)):
            # Rule 1: If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
            if stones[s] == 0:
                new_stones.append(1)
            else:
                # Rule 2: If the stone is engraved with a number that has an even number of digits, it is replaced by
                # two stones. The left half of the digits are engraved on the new left stone, and the right half of the
                # digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000
                # would become stones 10 and 0.)
                stone_str: str = str(stones[s])
                if len(stone_str) % 2 == 0:
                    new_left: str = stone_str[:len(stone_str) // 2]
                    new_right: str = stone_str[len(stone_str) // 2:]
                    new_stones.append(int(new_left))
                    new_stones.append(int(new_right))
                else:
                    # Rule 3: If none of the other rules apply, the stone is replaced by a new stone; the old stone's
                    # number multiplied by 2024 is engraved on the new stone.
                    new_stones.append(stones[s] * 2024)
        stones = new_stones

        logging.info(f'After {blink + 1} blinks, {len(stones)} stones = {stones[:50]}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
