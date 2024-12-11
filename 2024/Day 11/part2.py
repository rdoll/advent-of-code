#!/usr/bin/python3

#
# Advent of Code 2024 Day 11 Part Two
#

import argparse
import functools
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


@functools.cache
def blink(stone: int, num_blinks: int) -> int:
    if num_blinks == 0:
        return 1

    # Rule 1: If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    if stone == 0:
        return blink(1, num_blinks - 1)

    # Rule 2: If the stone is engraved with a number that has an even number of digits, it is replaced by
    # two stones. The left half of the digits are engraved on the new left stone, and the right half of the
    # digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000
    # would become stones 10 and 0.)
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        left_stone = int(stone_str[:len(stone_str) // 2])
        right_stone = int(stone_str[len(stone_str) // 2:])
        return blink(left_stone, num_blinks - 1) + blink(right_stone, num_blinks - 1)

    # Rule 3: If none of the other rules apply, the stone is replaced by a new stone; the old stone's
    # number multiplied by 2024 is engraved on the new stone.
    return blink(stone * 2024, num_blinks - 1)


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

    total: int = 0
    for stone in stones:
        logging.info(f'Starting stone {stone}')
        stone_total: int = blink(stone, args.blinks)
        total += stone_total
        logging.info(f'Stone {stone} generated {stone_total} stones, total now {total}')
    logging.info(f'Final total for {len(stones)} is {total}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
