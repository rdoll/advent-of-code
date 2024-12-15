#!/usr/bin/python3

#
# Advent of Code 2024 Day 15 Part One
#

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 15 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Warehouse:
    WALL: str = "#"
    EMPTY: str = "."
    BOX: str = "O"
    ROBOT: str = "@"

    UP: str = "^"
    RIGHT: str = ">"
    DOWN: str = "v"
    LEFT: str = "<"
    OFFSET: dict[str, tuple[int, int]] = {UP: (-1, 0), RIGHT: (0, 1), DOWN: (1, 0), LEFT: (0, -1)}

    def __init__(self):
        self.rows: int = 0
        self.cols: int = 0
        self.grid: list[list[str]] = []
        self.moves: list[str] = []

    def __str__(self):
        return f'dim={self.rows} x {self.cols}, num moves={len(self.moves)}'

    def print_grid(self):
        for row in self.grid:
            logging.info(f'    {"".join(row)}')

    def robot_pos(self) -> tuple[int, int]:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == self.ROBOT:
                    return r, c

    def load_input(self, input_file):
        for line in input_file:
            line = line.strip()
            if not line:
                continue

            if re.match(r'^#', line):
                self.rows += 1
                self.cols = len(line)
                self.grid.append(list(line))
            elif re.match(r'^[\^>v<]', line):
                for move in list(line):
                    self.moves.append(move)
            else:
                raise RuntimeError(f'Unknown line {line}')

    def move_robot(self, move: str):
        robot_pos: tuple[int, int] = self.robot_pos()
        offset: tuple[int, int] = self.OFFSET[move]
        end_pos: tuple[int, int] = robot_pos

        failsafe: int = max(self.rows, self.cols) + 1
        while True:
            end_pos = (end_pos[0] + offset[0], end_pos[1] + offset[1])
            end: str = self.grid[end_pos[0]][end_pos[1]]
            assert end != self.ROBOT, f'Duplicate robots at {robot_pos} and {end_pos}'
            if end == self.WALL:
                # the chain hits the wall, cannot move anything in chain
                logging.debug(f'Cannot move {move} from {robot_pos}, hit wall')
                return
            elif end == self.EMPTY:
                # walk back to robot moving everything up one
                logging.debug(f'Moving {move} robot {robot_pos} ending {end_pos}')
                while end_pos != robot_pos:
                    prior_pos: tuple[int, int] = (end_pos[0] - offset[0], end_pos[1] - offset[1])
                    self.grid[end_pos[0]][end_pos[1]] = self.grid[prior_pos[0]][prior_pos[1]]
                    self.grid[prior_pos[0]][prior_pos[1]] = self.EMPTY  # if prior is robot, leaves empty
                    end_pos = prior_pos
                return

            failsafe -= 1
            assert failsafe > 0, "move failsafe"

    def sum_box_gps(self) -> int:
        sum: int = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == self.BOX:
                     sum += r * 100 + c
        return sum


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    warehouse: Warehouse = Warehouse()
    warehouse.load_input(args.input_file[0])
    logging.info(f'warehouse = {warehouse}, robot_pos={warehouse.robot_pos()}')
    warehouse.print_grid()

    logging.info(f'Moving robot')
    for move in warehouse.moves:
        warehouse.move_robot(move)
    warehouse.print_grid()

    logging.info(f'Boxes GPS sum is {warehouse.sum_box_gps()}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
