#!/usr/bin/python3

#
# Advent of Code 2024 Day 14 Part One
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
    parser.add_argument('-s', '--seconds', metavar='#', type=int, default=100,
                        help='number of seconds to move robots')
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

    def add_robot(self, robot: Robot):
        self.robots.append(robot)

    def move_robots(self):
        for robot in self.robots:
            robot.move(self.width, self.height)

    def safety_factor(self) -> int:
        top_left: int = 0
        top_right: int = 0
        bottom_left: int = 0
        bottom_right: int = 0

        mx: int = self.width // 2
        my: int = self.height // 2

        for robot in self.robots:
            if robot.x < mx and robot.y < my:
                top_left += 1
            elif robot.x > mx and robot.y < my:
                top_right += 1
            elif robot.x < mx and robot.y > my:
                bottom_left += 1
            elif robot.x > mx and robot.y > my:
                bottom_right += 1
            else:
                logging.debug(f'Robot not in a quandrant {robot}')

        logging.info(f'Quandrant counts: tl={top_left}, tr={top_right}, bl={bottom_left}, br={bottom_right}')
        return top_left * top_right * bottom_left * bottom_right


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
    logging.info(f'Space is {args.x} by {args.y}, will simulate {args.seconds} seconds')

    space: Space = load_robots(args.input_file[0], args.x, args.y)
    logging.info(space)

    for s in range(args.seconds):
        space.move_robots()

    safety_factor: int = space.safety_factor()
    logging.info(f'Safety factor is {safety_factor}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
