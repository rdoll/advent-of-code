#!/usr/bin/python3

#
# Advent of Code 2024 Day 09 Part Two
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

    def first_free_range(self, file_id: int, file_start: int, size: int) -> int | None:
        # end_search = file_start - size + 1  # 6382582218798
        # end_search = file_start - size      # 6382582218798
        end_search = file_start             # 6382582136606   How is this better?!?
        # end_search = file_start + size  # 6382582136606 consider the file itself free????????
        for free_start in range(0, end_search):
            # if self.blocks[free_start] == Drive.FREE or self.blocks[free_start] == file_id:
            if self.blocks[free_start] == Drive.FREE:
                free_size: int = 1
                if size > 1:  # *** This was the check that cost me an hour of debugging!!!
                    for free_check in range(free_start + 1, end_search):
                        # if self.blocks[free_check] != Drive.FREE or self.blocks[free_start] == file_id:
                        if self.blocks[free_check] != Drive.FREE:
                            break
                        free_size += 1
                        if free_size == size:
                            break
                if free_size == size:
                    assert self.blocks[free_start - 1] != Drive.FREE, f'Cannot have free before free at {free_start}'
                    return free_start
        return None

    def validate_file(self, file_id: int, start: int, size: int):
        assert size in range(0, 10), f'File size {size} invalid for {file_id} at {start}'
        if start > 0:
            assert self.blocks[start - 1] != file_id, f'File {file_id} exists before start {start}'
        for b in range(start, start + size):
            assert self.blocks[b] == file_id, f'File {file_id} not found at {b}, start {start} size {size}'
        if start + size < len(self.blocks):
            assert self.blocks[start + size] != file_id, f'File {file_id} exists after end, {start} size {size}'

    def validate_free(self, file_id: int, start: int, size: int):
        assert size > 0, f'Free size {size} must be > 0'
        assert self.blocks[start] == Drive.FREE, f'Block {start} is not free, size {size}'
        for b in range(start, start + size):
            # assert self.blocks[b] == Drive.FREE or self.blocks[b] == file_id, \
            #     f'Block {b} is not free or {file_id}, start {start} size {size}'
            assert self.blocks[b] == Drive.FREE, f'Block {b} is not free, start {start} size {size}'

    def compact(self):
        compacted_files: set[int] = set()
        for block_num in range(len(self.blocks) - 1, -1, -1):
            file_id = self.blocks[block_num]
            if self.blocks[block_num] == Drive.FREE or file_id in compacted_files:
                continue
            compacted_files.add(file_id)

            size: int = 1
            file_start: int = block_num
            while file_start > 0:
                if self.blocks[file_start - 1] == file_id:
                    size += 1
                    file_start -= 1
                else:
                    break
            self.validate_file(file_id, file_start, size)

            free_start = self.first_free_range(file_id, file_start, size)
            if free_start:
                self.validate_free(file_id, free_start, size)
                for b in range(file_start, file_start + size):
                    assert self.blocks[b] == file_id, f'Cannot free block {b} with {self.blocks[b]} when should be {file_id}'
                    self.blocks[b] = Drive.FREE
                for b in range(free_start, free_start + size):
                    assert self.blocks[b] == Drive.FREE, f'Cannot move {file_id} over block {b} with {self.blocks[b]}'
                    self.blocks[b] = file_id
                self.validate_file(file_id, free_start, size)
                self.validate_free(file_id, file_start, size)
                logging.debug(f'Compacted file {file_id} at {file_start} to {free_start} with size {size}')
                self.print(logging.DEBUG)
            else:
                logging.debug(f'Could not compact {file_id} at {file_start} with size {size}')
        assert len(compacted_files) == self.next_file_id, f'Compacted {len(compacted_files)} but have {self.next_file_id} files'

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
    logging.info(f'Drive {drive}')
    drive.print()
    logging.info(f'Compacting drive')
    drive.compact()
    drive.print()
    checksum: int = drive.checksum()
    logging.info(f'Compacted drive has checksum {checksum}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
