#!/usr/bin/python3

import argparse
import logging
import re
import sys
from io import TextIOWrapper
from typing import List, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 09 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def read_positions(input_file: TextIOWrapper) -> List[Tuple[int, int]]:
    positions: List[Tuple[int, int]] = []

    for line in input_file:
        match: re.Match = re.match(r'^\s*(\d+),(\d+)\s*$', line.strip())
        if not match:
            logging.warning(f'Skipping unknown {line=}')
            continue
        positions.append((int(match.group(1)), int(match.group(2))))

    min_x = min(positions, key=lambda p: p[0])[0]
    min_y = min(positions, key=lambda p: p[1])[1]
    max_x = max(positions, key=lambda p: p[0])[0]
    max_y = max(positions, key=lambda p: p[1])[1]
    logging.info(f'{len(positions)=}, {min_x=}, {max_x=}, {min_y=}, {max_y=}')

    return positions


def calculate_area(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    width: int = abs(pos1[0] - pos2[0]) + 1
    height: int = abs(pos1[1] - pos2[1]) + 1
    return width * height


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    red_tile_positions = read_positions(args.input_file[0])

    largest_area: int = 0
    largest_area_pos1: Tuple[int, int] | None = None
    largest_area_pos2: Tuple[int, int] | None = None
    for pos1 in red_tile_positions:
        for pos2 in red_tile_positions:
            if pos1 == pos2:
                continue
            area: int = calculate_area(pos1, pos2)
            if area > largest_area:
                largest_area = area
                largest_area_pos1 = pos1
                largest_area_pos2 = pos2
    logging.info(f'{largest_area=}, {largest_area_pos1=}, {largest_area_pos2=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
