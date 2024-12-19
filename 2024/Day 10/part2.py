#!/usr/bin/python3

#
# Advent of Code 2024 Day 10 Part Two
#

import argparse
import functools
import logging
import re
import sys
from typing import Self


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 10 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Trail:
    def __init__(self, path: set[tuple[int, int]] = None):
        self.path: set[tuple[int, int]] = path if path else set()

    def __eq__(self, other):
        return self.path == other.visited

    def __hash__(self):
        return functools.reduce(lambda x, y: x + y, [hash(pos) for pos in self.path])

    def __str__(self):
        return f'Trail={self.path}'

    def __repr__(self):
        return f'Trail={self.path}'

    def copy(self) -> Self:
        path_copy: set[tuple[int, int]] = self.path.copy()
        return Trail(path_copy)

    def add(self, row: int, col: int):
        cell_pos: tuple[int, int] = (row, col)
        self.path.add(cell_pos)


class TopologyMap:
    NA_HEIGHT: int = -1
    NA_CHAR: str = "."
    TRAIL_OFFSETS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # North, East, South, West

    def __init__(self):
        self.target: int = 0
        self.rows: int = 0
        self.columns: int = 0
        self.map: list[list[int]] = []
        self.trailheads: dict[tuple[int, int], set[Trail]] = {}

    def __str__(self):
        return f'target={self.target}, rows={self.rows}, columns={self.columns}, num trailheads={len(self.trailheads)}'

    @staticmethod
    def cell(height: int):
        return TopologyMap.NA_CHAR if height == TopologyMap.NA_HEIGHT else str(height)

    @staticmethod
    def height_value(cell: str):
        return TopologyMap.NA_HEIGHT if cell == TopologyMap.NA_CHAR else int(cell)

    def print(self, level: int = logging.INFO):
        for row in self.map:
            logging.log(level=level, msg=f'    {"".join([self.cell(col) for col in row])}')

    def add_heights(self, heights: list[int]):
        if self.columns > 0:
            assert len(heights) == self.columns, f'Cannot change number of columns'
        else:
            self.columns = len(heights)
        self.rows += 1
        self.map.append(heights)

    def follow_trail(self, next_height: int, row: int, col: int, trail: Trail) -> set[Trail]:
        if row not in range(0, self.rows) or col not in range(0, self.columns):
            return set()

        if self.map[row][col] != next_height:
            return set()  # trail cannot continue at this row/col

        all_trails: set[Trail] = set()
        if next_height == 9:
            full_trail: Trail = trail.copy()
            full_trail.add(row, col)
            all_trails.add(full_trail)
        else:
            for offset in TopologyMap.TRAIL_OFFSETS:
                offset_trail: Trail = trail.copy()
                offset_trail.add(row, col)
                offset_trails: set[Trail] = self.follow_trail(next_height + 1, row + offset[0], col + offset[1], offset_trail)
                all_trails.update(offset_trails)
        return all_trails

    def add_trails(self, head_row: int, head_col: int, trails: set[Trail]):
        head_pos = (head_row, head_col)
        if len(trails) > 0:
            logging.debug(f'Trailhead at {head_pos} had trails {trails}')
            if not head_pos in self.trailheads:
                self.trailheads[head_pos] = set()
            self.trailheads[head_pos].update(trails)

    def find_trails(self):
        for r in range(0, self.rows):
            for c in range(0, self.columns):
                if self.map[r][c] == 0:
                    for offset in TopologyMap.TRAIL_OFFSETS:
                        trail: Trail = Trail()
                        trail.add(r, c)
                        trails: set[Trail] = self.follow_trail(1, r + offset[0], c + offset[1], trail)
                        self.add_trails(r, c, trails)

    def trailheads_score(self) -> int:
        score: int = 0
        for trails in self.trailheads.values():
            score += len(trails)
        return score


def load_map(input_file) -> TopologyMap:
    topology_map: TopologyMap = TopologyMap()
    lines: int = 0
    for line in input_file:
        line = line.strip()
        if not line:
            continue

        if re.match(r'^\s*#', line):
            topology_map.target = int(re.findall(r'\sscore\s*=\s*(\d+)', line)[0])
            logging.debug(f'Found target score {topology_map.target}')
            continue

        heights: list[int] = [TopologyMap.height_value(cell) for cell in list(line)]
        topology_map.add_heights(heights)

    return topology_map


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    topology_map = load_map(args.input_file[0])
    logging.info(f'TopologyMap {topology_map}')
    topology_map.print()
    topology_map.find_trails()
    logging.info(f'TopologyMap {topology_map}')
    score = topology_map.trailheads_score()
    if topology_map.target > 0:
        assert score == topology_map.target, f'Score {score} does not match target {topology_map.target}'
    logging.info(f'Trailhead score {score}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
