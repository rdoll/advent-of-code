#!/usr/bin/python3

#
# Advent of Code 2024 Day 14 Part Two
#

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 14 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-x', '--x', metavar='#', type=int, required=True,
                        help='how many tiles wide the space is')
    parser.add_argument('-y', '--y', metavar='#', type=int, required=True,
                        help='how many tiles high the space is')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Robot:
    def __init__(self, x: int, y: int, dx: int, dy: int):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __str__(self):
        return f'p={self.x},{self.y} v={self.dx},{self.dy}'

    def move(self, width: int, height: int):
        self.x += self.dx
        if self.x < 0:
            self.x += width
        elif self.x >= width:
            self.x -= width

        self.y += self.dy
        if self.y < 0:
            self.y += height
        elif self.y >= height:
            self.y -= height


class Space:
    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.robots: list[Robot] = []

    def __str__(self):
        return (f'grid={self.width}x{self.height}, num robots={len(self.robots)}')

    def grid_cell(self, count: int) -> str:
        if count == 0:
            return "."
        if count > 9:
            return "*"
        return str(count)

    def build_grid(self) -> list[list[int]]:
        grid: list[list[int]] = []
        for x in range(self.width):
            grid.append([0 for y in range(self.height)])

        for robot in self.robots:
            grid[robot.x][robot.y] += 1

        return grid

    def print_grid(self):
        grid: list[list[int]] = self.build_grid()
        for x in range(self.width):
            logging.info(f'    {"".join([self.grid_cell(grid[x][y]) for y in range(self.height)])}')

    def add_robot(self, robot: Robot):
        self.robots.append(robot)

    def move_robots(self):
        for robot in self.robots:
            robot.move(self.width, self.height)

    def is_xmas_tree(self) -> bool:
        # I really dislike this challenge. I have no idea what shape to look for.
        # My dumb guess is to look for a large number of robots in a line and I'll look at the grid to confirm.
        grid = self.build_grid()

        # horizontal line
        for y in range(self.height):
            for x in range(self.width - 10):
                if grid[x][y] > 0:
                    line: bool = True
                    for i in range(10):
                        if grid[x + i][y] == 0:
                            line = False
                            break
                    if line:
                        return True

        return False


def load_robots(input_file, width: int, height: int) -> Space:
    space: Space = Space(width, height)
    for line in input_file:
        line = line.strip()
        if not line:
            continue

        [x, y, dx, dy] = [int(n) for n in list(re.findall(r'p=(\d+),(\d+)\s+v=(-?\d+),(-?\d+)', line)[0])]
        assert x is not None and x in range (width), f'invalid x position {x}'
        assert y is not None and y in range (height), f'invalid y position {y}'
        assert dx is not None, f'invalid dx {dx}'
        assert dy is not None, f'invalid dy {dy}'
        robot: Robot = Robot(x, y, dx, dy)
        space.add_robot(robot)
        logging.debug(f'Loaded robot {robot}')

    return space


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.info(f'Space is {args.x} by {args.y}')

    space: Space = load_robots(args.input_file[0], args.x, args.y)
    logging.info(space)

    seconds: int = 0
    while not space.is_xmas_tree():
        seconds += 1
        if seconds % 2000 == 0:
            logging.debug(f'Seconds elapsed {seconds}')
        elif seconds > 10000:
            raise RuntimeError(f'Exceeded max seconds')
        space.move_robots()
        # space.print_grid()

    space.print_grid()
    logging.info(f'Xmas tree after {seconds} seconds')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
