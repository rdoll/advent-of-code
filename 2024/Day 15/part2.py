#!/usr/bin/python3

#
# Advent of Code 2024 Day 15 Part Two
#

import argparse
import logging
import re
import sys
from copy import deepcopy


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
    BOXL: str = "["
    BOXR: str = "]"
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

    def grid_around(self, move_grid: list[list[str]], pos: tuple[int, int], radius: int) -> list[str]:
        s: list[str] = []
        for row in move_grid[pos[0] - radius:pos[0] + radius + 1]:
            s.append("".join(row[pos[1] - radius:pos[1] + radius + 1]))
        return s

    def validate(self):
        robots: int = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == self.BOXL and self.grid[r][c+1] != self.BOXR:
                    self.print_grid()
                    raise RuntimeError(f'Box left at {(r, c)} missing box right')
                elif self.grid[r][c] == self.BOXR and self.grid[r][c-1] != self.BOXL:
                    self.print_grid()
                    raise RuntimeError(f'Box right at {(r, c)} missing box left')
                elif self.grid[r][c] == self.ROBOT:
                    robots += 1
        if robots != 1:
            raise RuntimeError(f'Wrong number of robots {robots}')

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
                self.cols = 2 * len(line)
                row: list[str] = []
                for i in range(len(line)):
                    if line[i] == self.ROBOT:
                        row.append(self.ROBOT)
                        row.append(self.EMPTY)
                    elif line[i] == self.BOX:
                        row.append(self.BOXL)
                        row.append(self.BOXR)
                    else:
                        row.append(line[i])
                        row.append(line[i])
                self.grid.append(row)
            elif re.match(r'^[\^>v<]', line):
                for move in list(line):
                    self.moves.append(move)
            else:
                raise RuntimeError(f'Unknown line {line}')

    def move_robot_horiz(self, move: str):
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

    def move_box_vert(self, move_grid: list[list[str]], boxl_pos: tuple[int, int], move: str) -> bool:
        offset: tuple[int, int] = self.OFFSET[move]
        boxl: str = move_grid[boxl_pos[0]][boxl_pos[1]]
        assert boxl == self.BOXL, f'Must be box left {boxl_pos} move {move}'

        boxr_pos: tuple[int, int] = (boxl_pos[0], boxl_pos[1] + 1)
        boxr: str = move_grid[boxr_pos[0]][boxr_pos[1]]
        assert boxr == self.BOXR, f'Must be box right for box at {boxl_pos} move {move}'

        nextl_pos: tuple[int, int] = (boxl_pos[0] + offset[0], boxl_pos[1] + offset[1])
        nextl: str = move_grid[nextl_pos[0]][nextl_pos[1]]
        if nextl == self.WALL:
            return False
        elif nextl == self.BOXL:
            if not self.move_box_vert(move_grid, nextl_pos, move):
                return False
        elif nextl == self.BOXR:
            if not self.move_box_vert(move_grid, (nextl_pos[0], nextl_pos[1] - 1), move):
                return False
        nextl = move_grid[nextl_pos[0]][nextl_pos[1]]
        assert nextl == self.EMPTY, f'Not empty for box left move {boxl_pos}'

        nextr_pos: tuple[int, int] = (boxr_pos[0] + offset[0], boxr_pos[1] + offset[1])
        nextr: str = move_grid[nextr_pos[0]][nextr_pos[1]]
        if nextr == self.WALL:
            return False
        elif nextr == self.BOXL:
            if not self.move_box_vert(move_grid, nextr_pos, move):
                return False
        elif nextr == self.BOXR:
            if not self.move_box_vert(move_grid, (nextr_pos[0], nextr_pos[1] - 1), move):
                return False
        nextr = move_grid[nextr_pos[0]][nextr_pos[1]]
        assert nextr == self.EMPTY, f'Not empty for box right move {boxl_pos}'

        move_grid[nextl_pos[0]][nextl_pos[1]] = self.BOXL
        move_grid[boxl_pos[0]][boxl_pos[1]] = self.EMPTY
        move_grid[nextr_pos[0]][nextr_pos[1]] = self.BOXR
        move_grid[boxr_pos[0]][boxr_pos[1]] = self.EMPTY
        return True

    def move_robot_vert(self, move_grid: list[list[str]], robot_pos: tuple[int, int], move: str) -> bool:
        offset: tuple[int, int] = self.OFFSET[move]
        next_pos: tuple[int, int] = (robot_pos[0] + offset[0], robot_pos[1] + offset[1])
        next: str = move_grid[next_pos[0]][next_pos[1]]

        if next == self.WALL:
            return False
        elif next == self.BOXL:
            if not self.move_box_vert(move_grid, next_pos, move):
                return False
        elif next == self.BOXR:
            if not self.move_box_vert(move_grid, (next_pos[0], next_pos[1] - 1), move):
                return False

        next: str = move_grid[next_pos[0]][next_pos[1]]
        assert next == self.EMPTY, f'Not empty for robot move {robot_pos}'
        move_grid[next_pos[0]][next_pos[1]] = self.ROBOT
        move_grid[robot_pos[0]][robot_pos[1]] = self.EMPTY
        return True

    def move_robot(self, move: str):
        if move == self.RIGHT or move == self.LEFT:
            self.move_robot_horiz(move)
        else:
            move_grid: list[list[str]] = deepcopy(self.grid)
            robot_pos: tuple[int, int] = self.robot_pos()
            if self.move_robot_vert(move_grid, robot_pos, move):
                logging.debug(f'Moved {move} from {robot_pos}')
                self.grid = move_grid
            else:
                logging.debug(f'Cannot move {move} from {robot_pos}')
        self.validate()

    def sum_box_gps(self) -> int:
        sum: int = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == self.BOXL:
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
