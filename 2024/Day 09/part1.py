#!/usr/bin/python3

#
# Advent of Code 2024 Day 09 Part One
#

import argparse
import logging
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 09 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Drive:
    FILE_ID_CHARS: str = "0123456789abcdefghijklmnopqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWYXZ"
    FILE_ID_TOO_LARGE: str = "!"
    FREE: int = -1

    def __init__(self):
        self.next_file_id: int = 0
        self.blocks: list[int] = []

    def __str__(self):
        return f'next_file_id={self.next_file_id}, num blocks={len(self.blocks)}'

    def block_char(self, file_id: int):
        if file_id == Drive.FREE:
            return "."
        elif file_id >= len(Drive.FILE_ID_CHARS):
            return Drive.FILE_ID_TOO_LARGE
        else:
            return list(Drive.FILE_ID_CHARS)[file_id]

    def print(self, level: int = logging.INFO):
        logging.log(level=level, msg=f'    {"".join([self.block_char(file_id) for file_id in self.blocks[0:200]])}')

    def add_file(self, size: int):
        assert size > 0, f'File cannot be zero or less {size}'
        for s in range(0, size):
            self.blocks.append(self.next_file_id)
        self.next_file_id += 1

    def add_free(self, size: int):
        for s in range(0, size):
            self.blocks.append(Drive.FREE)

    def first_free_block_num(self) -> int:
        for block_num in range(0, len(self.blocks)):
            if self.blocks[block_num] == Drive.FREE:
                return block_num
        raise RuntimeError(f'No free blocks found in drive {self}')

    def compact(self):
        for block_num in range(len(self.blocks) - 1, -1, -1):
            if self.blocks[block_num] == Drive.FREE:
                continue
            first_free = self.first_free_block_num()
            if first_free < block_num:
                self.blocks[first_free] = self.blocks[block_num]
                self.blocks[block_num] = Drive.FREE

    def checksum(self) -> int:
        checksum: int = 0
        for block_num in range(0, len(self.blocks)):
            if self.blocks[block_num] != Drive.FREE:
                checksum += block_num * self.blocks[block_num]
        return checksum


def load_drive_map(input_file) -> Drive:
    drive: Drive = Drive()
    lines: int = 0
    for line in input_file:
        line = line.strip()
        if not line:
            continue

        if lines >= 1:
            raise RuntimeError(f'Input file can only contain one meaningful line')
        lines += 1

        map: list[int] = [int(digit) for digit in list(line)]
        next_is_file: bool = True
        for digit in map:
            assert digit in range(0, 10), f'Unknown character in drive map {digit}'
            if next_is_file:
                drive.add_file(digit)
                next_is_file = False
            else:
                drive.add_free(digit)
                next_is_file = True

    return drive


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    drive = load_drive_map(args.input_file[0])
    logging.debug(f'Drive {drive}')
    drive.print()
    drive.compact()
    drive.print()
    checksum: int = drive.checksum()
    logging.info(f'Compacted drive has checksum {checksum}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
