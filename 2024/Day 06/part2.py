#!/usr/bin/python3

#
# Advent of Code 2024 Day 06 Part Two
#

import argparse
import copy
import logging
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 06 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class World:
    EMPTY: str = "."
    OBSTACLE: str = "#"
    GUARD_UP: str = "^"
    GUARD_RIGHT: str = ">"
    GUARD_DOWN: str = "v"
    GUARD_LEFT: str = "<"
    GUARDS: list[str] = [GUARD_UP,  GUARD_RIGHT, GUARD_DOWN, GUARD_LEFT]
    VISITED: str = "X"
    NEW_BLOCK: str = "O"

    GUARD_PATH = {
        GUARD_UP:    {'offset': (-1,  0), 'next_guard': GUARD_RIGHT, 'loop_check_offset': ( 0,  1)},
        GUARD_RIGHT: {'offset': ( 0,  1), 'next_guard': GUARD_DOWN,  'loop_check_offset': ( 1,  0)},
        GUARD_DOWN:  {'offset': ( 1,  0), 'next_guard': GUARD_LEFT,  'loop_check_offset': ( 0, -1)},
        GUARD_LEFT:  {'offset': ( 0, -1), 'next_guard': GUARD_UP,    'loop_check_offset': (-1,  0)}
    }


    def __init__(self, grid: list[list[str]]):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])
        self.guard_pos = self.find_guard()
        self.guard = self.grid[self.guard_pos[0]][self.guard_pos[1]]


    def debug_log_grid(self):
        for row in range(0, self.rows):
            logging.debug(f'  {"".join(self.grid[row])}')
        logging.debug("")


    def find_guard(self) -> tuple[int, int] | None:
        for r in range(0, len(self.grid)):
            for c in range(0, len(self.grid[r])):
                if self.grid[r][c] in self.GUARDS:
                    logging.debug(f'Guard found at {(r, c)}')
                    return r, c
        return None


    def is_in_grid(self, pos: tuple[int, int]):
        return pos[0] in range(0, self.rows) and pos[1] in range(0, self.columns)


    def move_forward(self) -> bool:
        self.guard = self.grid[self.guard_pos[0]][self.guard_pos[1]]
        [offset, next_guard, loop_check_offset] = self.GUARD_PATH[self.guard].values()

        for failsafe in range(0, max(self.rows, self.columns) + 1):
            self.grid[self.guard_pos[0]][self.guard_pos[1]] = self.VISITED

            next_pos = (self.guard_pos[0] + offset[0], self.guard_pos[1] + offset[1])
            if not self.is_in_grid(next_pos):
                logging.info(f'Guard exited grid moving {self.guard} at {self.guard_pos}')
                #self.debug_log_grid()
                return True

            next = self.grid[next_pos[0]][next_pos[1]]
            if next == self.OBSTACLE:
                # guard stops before obstacle and turns
                self.grid[self.guard_pos[0]][self.guard_pos[1]] = next_guard
                self.guard = next_guard
                logging.debug(f'Guard {self.guard} moved to {self.guard_pos}')
                return False
            elif next == self.EMPTY or next == self.VISITED or next == self.NEW_BLOCK:
                # guard moves into position
                self.guard_pos = next_pos
                self.grid[self.guard_pos[0]][self.guard_pos[1]] = self.guard
            else:
                raise RuntimeError(f'Unexpected grid character {next} at {next_pos}')

        raise RuntimeError(f'Failsafe hit while moving guard {self}')


    def move_full_path(self):
        failsafe = self.rows * self.columns
        while failsafe > 0:
            finished = self.move_forward()
            if finished:
                break
            #self.debug_log_grid()

            failsafe -= 1
            if failsafe <= 0:
                raise OverflowError(f'Guard trips exceeded failsafe -- presume this is a loop!')

        assert self.find_guard() is None, f'Guard is still in grid!'

        visited: int = 0
        for row in self.grid:
            for col in row:
                if col == self.VISITED:
                    visited += 1
        logging.debug(f'Guard visited {visited} positions')


def load_grid(input_file) -> list[list[str]]:
    rows: int = 0
    columns: int = 0
    grid: list[list[str]] = []
    for line in input_file:
        line = line.strip()
        if not line:
            continue

        rows += 1
        row = list(line)
        if columns > 0:
            if len(row) != columns:
                raise RuntimeError(f'In row {rows}, number of columns changed from {columns} to {len(row)}')
        else:
            columns = len(row)
        grid.append(row)

    logging.debug(f'Read {rows} x {columns} grid')
    return grid


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    grid = load_grid(args.input_file[0])
    loops: int = 0
    for r in range(0, len(grid)):
        for c in range(0, len(grid[r])):
            if grid[r][c] == World.EMPTY:
                # if an obstacle was placed here, would guard still path to exit or loop?
                world = World(copy.deepcopy(grid))
                world.grid[r][c] = World.OBSTACLE
                try:
                    world.move_full_path()
                    logging.info(f'No loop with extra obstacle at {(r, c)}')
                except OverflowError as e:
                    logging.info(f'Loop detected with extra obstacle at {(r, c)}')
                    loops += 1
    logging.info(f'Placing {loops} single obstacles can create a loop')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
