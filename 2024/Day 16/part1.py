#!/usr/bin/python3

#
# Advent of Code 2024 Day 16 Part One
#

import argparse
import copy
import logging
import sys
from typing import Self


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 16 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Path:
    def __init__(self):
        self.score: int = 0
        self.path: dict[tuple[int, int, str], int] = {}  # used as an ordered set

    def __str__(self):
        return f'score={self.score}, path={self.path}'

    def would_loop(self, pos3: tuple[int, int, str]) -> bool:
        return pos3 in self.path

    def add(self, pos3: tuple[int, int, str], cost: int):
        assert pos3 not in self.path, f'Cannot add loop {pos3} to path {self.path}'
        self.path[pos3] = 0
        self.score += cost


class Maze:
    WALL: str = "#"
    EMPTY: str = "."
    START: str = "S"
    END: str = "E"

    MOVE_COST: int = 1
    TURN_COST: int = 1000

    NORTH: str = "^"
    EAST:  str = ">"
    SOUTH: str = "v"
    WEST:  str = "<"
    FACING_MAP: dict[str, dict[str, tuple[int, int] | str]] = {
        NORTH: {'offset': (-1,  0), 'ccw': WEST,  'cw': EAST},
        EAST:  {'offset': ( 0,  1), 'ccw': NORTH, 'cw': SOUTH},
        SOUTH: {'offset': ( 1,  0), 'ccw': EAST,  'cw': WEST},
        WEST:  {'offset': ( 0, -1), 'ccw': SOUTH, 'cw': NORTH}
    }

    def __init__(self):
        self.rows: int = 0
        self.cols: int = 0
        self.grid: list[list[str]] = []
        self.start_pos3: tuple[int, int, str] | None = None
        self.end_pos: tuple[int, int] | None = None
        self.path_cache: dict[tuple[int, int, str], Path | None] = {}

    def __str__(self):
        return f'dim={self.rows} x {self.cols}, start={self.start_pos3}, end={self.end_pos}'

    def print_grid(self, level: int = logging.INFO, grid: list[list[str]] = None):
        for row in self.grid if grid is None else grid:
            logging.log(level=level, msg=f'  {"".join(row)}')

    def print_path(self, path: Path, level: int = logging.INFO):
        grid: list[list[str]] = copy.deepcopy(self.grid)
        for pos3 in path.path:
            if pos3 != self.start_pos3 and (pos3[0], pos3[1]) != self.end_pos:
                grid[pos3[0]][pos3[1]] = pos3[2]
        self.print_grid(level=level, grid=grid)

    def find_landmarks(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == self.START:
                    assert self.start_pos3 is None, f'Two starts!'
                    self.start_pos3 = (r, c, self.EAST)
                if self.grid[r][c] == self.END:
                    assert self.end_pos is None, f'Two ends!'
                    self.end_pos = (r, c)

    def load_input(self, input_file):
        for line in input_file:
            line = line.strip()
            if not line:
                continue

            self.rows += 1
            self.cols = len(line)
            self.grid.append(list(line))

        self.find_landmarks()

    def move(self, pos3: tuple[int, int, str], cost: int, path: Path, depth: int) -> Path | None:
        if pos3 in self.path_cache:
            return self.path_cache[pos3]

        assert depth < self.rows * self.cols + 1, f'depth={depth} is too high!'

        cell: str = self.grid[pos3[0]][pos3[1]]

        # check if move rejected
        if cell == self.WALL:
            return None
        if path.would_loop(pos3):
            logging.debug(f'Would loop {pos3} for {path}')
            return None

        # move accepted
        path.add(pos3, cost)
        if cell == self.END:
            logging.debug(f'Reached end {pos3}')
            return path

        # next move forward
        fwd_facing: str = pos3[2]
        fwd_map: dict[str, tuple[int, int] | str] = self.FACING_MAP[fwd_facing]
        fwd_offset: tuple[int, int] = fwd_map['offset']
        fwd_pos3: tuple[int, int, str] = (pos3[0] + fwd_offset[0], pos3[1] + fwd_offset[1], fwd_facing)
        fwd_path: Path = copy.deepcopy(path)
        fwd_result: Path | None = self.move(fwd_pos3, self.MOVE_COST, fwd_path, depth + 1)
        # assert fwd_pos3 not in self.path_cache, f'Already have {fwd_pos3} in path cache'
        self.path_cache[fwd_pos3] = fwd_result

        # next turn counterclockwise then move forward
        ccw_facing: str = fwd_map['ccw']
        ccw_map: dict[str, tuple[int, int] | str] = self.FACING_MAP[ccw_facing]
        ccw_offset: tuple[int, int] = ccw_map['offset']
        ccw_pos3: tuple[int, int, str] = (pos3[0] + ccw_offset[0], pos3[1] + ccw_offset[1], ccw_facing)
        ccw_path: Path = copy.deepcopy(path)
        ccw_result: Path | None = self.move(ccw_pos3, self.TURN_COST + self.MOVE_COST, ccw_path, depth + 1)
        # assert ccw_pos3 not in self.path_cache, f'Already have {ccw_pos3} in path cache'
        self.path_cache[ccw_pos3] = ccw_result

        # next turn clockwise then move forward
        cw_facing: str = fwd_map['cw']
        cw_map: dict[str, tuple[int, int] | str] = self.FACING_MAP[cw_facing]
        cw_offset: tuple[int, int] = cw_map['offset']
        cw_pos3: tuple[int, int, str] = (pos3[0] + cw_offset[0], pos3[1] + cw_offset[1], cw_facing)
        cw_path: Path = copy.deepcopy(path)
        cw_result: Path | None = self.move(cw_pos3, self.TURN_COST + self.MOVE_COST, cw_path, depth + 1)
        # assert cw_pos3 not in self.path_cache, f'Already have {cw_pos3} in path cache'
        self.path_cache[cw_pos3] = cw_result

        min_score: int = min(fwd_result.score if fwd_result is not None else 10**20,
                             ccw_result.score if ccw_result is not None else 10**20,
                             cw_result.score if cw_result is not None else 10**20)
        if fwd_result is not None and fwd_result.score == min_score:
            return fwd_result
        if ccw_result is not None and ccw_result.score == min_score:
            return ccw_result
        if cw_result is not None and cw_result.score == min_score:
            return cw_result
        return None

    def find_path(self) -> Path:
        path: Path = self.move(self.start_pos3, 0, Path(), 0)
        assert path is not None, f'Could not find path!'
        return path


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    maze: Maze = Maze()
    maze.load_input(args.input_file[0])
    logging.info(f'maze = {maze}')
    maze.print_grid()

    path: Path = maze.find_path()
    maze.print_path(path)
    logging.info(f'Found lowest score path = {path}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
