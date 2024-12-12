#!/usr/bin/python3

#
# Advent of Code 2024 Day 12 Part One
#

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 12 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Region:
    def __init__(self, id: int, plant: str, cell: tuple[int, int] = None):
        self.id: int = id
        self.plant: str = plant
        self.cells: set[tuple[int, int]] = set()
        self.perimeter: int = 0
        self.area: int = 0
        self.price: int = 0

        if cell is not None:
            self.cells.add(cell)

    def __str__(self):
        return (f'id={self.id}, plant={self.plant}, perimeter={self.perimeter}, area={self.area}, price={self.price},'
                f' cells={self.cells}')


class Garden:
    GROW_OFFSETS: list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # up, right, down, left

    def __init__(self):
        self.rows: int = 0
        self.columns: int = 0
        self.grid: list[list[str]] = []
        self.target_price: int = 0
        self.last_region_id: int = 0
        self.regions: dict[int, Region] = {}
        self.region_map: list[list[Region | None]] = []

    def __str__(self):
        return (f'Size {self.rows} x {self.columns}, target_price={self.target_price}, last_region_id={self.last_region_id}')

    def print_grid(self, level: int = logging.INFO):
        for row in self.grid:
            logging.log(level=level, msg=f'    {"".join(col for col in row)}')

    def load(self, input_file):
        for line in input_file:
            line = line.strip()
            if not line:
                continue

            if re.match(r'^\s*#', line):
                self.target_price = int(re.findall(r'\sprice\s*=\s*(\d+)', line)[0])
                logging.debug(f'Found target price {self.target_price}')
                continue

            plants: list[str] = list(line)
            if self.columns > 0:
                assert self.columns == len(plants), f'Already read {self.columns} columns, but row {self.rows} had {len(plants)}'
            else:
                self.columns = len(plants)
            self.rows += 1
            self.grid.append(plants)
            self.region_map.append([None for c in range(self.columns)])

    def grow_region(self, region: Region, row: int, column: int, depth: int):
        assert depth <= self.rows * self.columns, f'Cannot grow region beyond # cells in grid!'
        assert (row, column) in region.cells, f'Cannot grow cell not in region!'
        for offset in Garden.GROW_OFFSETS:
            r = row + offset[0]
            c = column + offset[1]
            if r not in range(self.rows) or c not in range(self.columns):
                # can't grow outside of garden boundary
                continue
            if self.region_map[r][c] is not None:
                # cell is already part of another region
                continue
            if self.grid[r][c] != region.plant:
                # different plant at this cell
                continue

            # plant is part of our region
            region.cells.add( (r, c) )
            self.region_map[r][c] = region
            self.grow_region(region, r, c, depth + 1)

    def calculate_price(self, region):
        region.area = len(region.cells)
        region.perimeter = 0
        for cell in region.cells:
            for offset in Garden.GROW_OFFSETS:
                r: int = cell[0] + offset[0]
                c: int = cell[1] + offset[1]
                if r not in range(self.rows) or c not in range(self.columns):
                    # grid edges are part of the perimeter
                    region.perimeter += 1
                elif (r, c) not in region.cells:
                    # offset cell is not part of this region, so this is a perimeter edge
                    region.perimeter += 1
                else:
                    # offset cell is in this region, so this edge is not part of the perimiter
                    region.perimeter += 0
        region.price = region.area * region.perimeter

    def find_regions(self):
        for r in range(self.rows):
            for c in range(self.columns):
                plant: str = self.grid[r][c]
                if self.region_map[r][c] is None:
                    self.last_region_id += 1
                    region: Region = Region(self.last_region_id, plant, (r, c))
                    self.regions[region.id] = region
                    self.region_map[r][c] = region
                    self.grow_region(region, r, c, 0)
                    self.calculate_price(region)
                    logging.debug(f'Grew and calculated region {region}')


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    garden: Garden = Garden()
    garden.load(args.input_file[0])
    logging.info(garden)
    garden.print_grid()

    garden.find_regions()

    total_price: int = sum([region.price for region in garden.regions.values()])
    logging.info(f'Actual total price {total_price}, expected target price {garden.target_price}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
