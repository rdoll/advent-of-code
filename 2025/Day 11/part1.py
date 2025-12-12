#!/usr/bin/python3

import argparse
import logging
import re
import sys
from typing import List, Dict


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 11 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


def trace_path(devices: Dict[str, List[str]], path: List[str]) -> int:
    device: str = path[-1]
    if device == 'out':
        logging.debug(f'Found {path=}')
        return 1

    found: int = 0
    for connection in devices[device]:
        if not connection in path:
            new_path: List[str] = list(path)
            new_path.append(connection)
            found += trace_path(devices, new_path)
    return found


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    devices: Dict[str, List[str]] = {}
    for line in args.input_file[0]:
        match: re.Match = re.match(r'^\s*(\S+):\s*(.*)\s*$', line.strip())
        if not match:
            logging.warning(f'Skipping invalid {line=}')
            continue
        device: str = match.group(1)
        connections: List[str] = match.group(2).split()
        devices[device] = connections
    logging.debug(f'Found {len(devices)} {devices=}')

    total: int = trace_path(devices, ['you'])
    logging.info(f'Final total: {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
