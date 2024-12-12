#!/usr/bin/python3

#
# Advent of Code 2024 Day 12 Part Two
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
        self.sides: int = 0
        self.area: int = 0
        self.price: int = 0

        if cell is not None:
            self.cells.add(cell)

    def __str__(self):
        return (f'id={self.id}, plant={self.plant}, sides={self.sides}, area={self.area}, price={self.price},'
                f' cells={self.cells}')


class Garden:
    OFFSET_NORTH: tuple[int, int] = (-1,  0)
    OFFSET_EAST:  tuple[int, int] = ( 0,  1)
    OFFSET_SOUTH: tuple[int, int] = ( 1,  0)
    OFFSET_WEST:  tuple[int, int] = ( 0, -1)
    GROW_OFFSETS: list[tuple[int, int]] = [OFFSET_NORTH, OFFSET_EAST, OFFSET_SOUTH, OFFSET_WEST]

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

    def find_row_sides(self, side_offset: tuple[int, int]):
        last_region_id: int = -1
        last_had_side: bool = False
        for row in range(self.rows):
            for column in range(self.columns):
                region = self.region_map[row][column]
                r = row + side_offset[0]
                c = column + side_offset[1]
                if r not in range(self.rows) or c not in range(self.columns):
                    if last_region_id == region.id and last_had_side:
                        # at grid edge and previous region was us and it had a side, so continue it
                        continue
                    else:
                        # at grid edge and there was no previous side or the previous side was for a different region;
                        # either way, new side!
                        region.sides += 1
                        last_region_id = region.id
                        last_had_side = True
                else:
                    side_region: Region = self.region_map[r][c]
                    if side_region.id == region.id:
                        # side check cell is in our same region, so no perimeter side
                        last_region_id = region.id
                        last_had_side = False
                        continue
                    elif last_region_id == region.id and last_had_side:
                        # side check cell is different region and our previous was the same region and had a side,
                        # so the same side continues here
                        continue
                    else:
                        # side check cell is different region and either there was no previous side or the previous
                        # side was for a different region; either way, new side!
                        region.sides += 1
                        last_region_id = region.id
                        last_had_side = True

            # don't continue previous region across rows
            last_region_id = -1
            last_had_side = False

    # Yes, this should be basically a cut-and-paste of find_row_sides
    def find_column_sides(self, side_offset: tuple[int, int]):
        last_region_id: int = -1
        last_had_side: bool = False
        for column in range(self.columns):
            for row in range(self.rows):
                region = self.region_map[row][column]
                r = row + side_offset[0]
                c = column + side_offset[1]
                if r not in range(self.rows) or c not in range(self.columns):
                    if last_region_id == region.id and last_had_side:
                        # at grid edge and previous region was us and it had a side, so continue it
                        continue
                    else:
                        # at grid edge and there was no previous side or the previous side was for a different region;
                        # either way, new side!
                        region.sides += 1
                        last_region_id = region.id
                        last_had_side = True
                else:
                    side_region: Region = self.region_map[r][c]
                    if side_region.id == region.id:
                        # side check cell is in our same region, so no perimeter side
                        last_region_id = region.id
                        last_had_side = False
                        continue
                    elif last_region_id == region.id and last_had_side:
                        # side check cell is different region and our previous was the same region and had a side,
                        # so the same side continues here
                        continue
                    else:
                        # side check cell is different region and either there was no previous side or the previous
                        # side was for a different region; either way, new side!
                        region.sides += 1
                        last_region_id = region.id
                        last_had_side = True

            # don't continue previous region across rows
            last_region_id = -1
            last_had_side = False

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
                    logging.debug(f'Grew region {region}')

    def calculate_prices(self):
        self.find_row_sides(Garden.OFFSET_NORTH)
        self.find_row_sides(Garden.OFFSET_SOUTH)
        self.find_column_sides(Garden.OFFSET_EAST)
        self.find_column_sides(Garden.OFFSET_WEST)

        for region in self.regions.values():
            region.area = len(region.cells)
            region.price = region.area * region.sides
            logging.debug(f'Calculated price of region {region}')


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
    garden.calculate_prices()
    total_price: int = sum([region.price for region in garden.regions.values()])
    logging.info(f'Actual total price {total_price}, expected target price {garden.target_price}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
