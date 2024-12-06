#!/usr/bin/python3

#
# Advent of Code 2024 Day 06 Part Two
#

import argparse
import logging
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 06 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-m', '--max-lines', metavar='#', type=int, default=0,
                        help='constrain input to this many lines, 0 = disabled')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


EMPTY: str = "."
OBSTACLE: str = "#"
GUARD_UP: str = "^"
GUARD_RIGHT: str = ">"
GUARD_DOWN: str = "v"
GUARD_LEFT: str = "<"
GUARDS: list[str] = [GUARD_UP,  GUARD_RIGHT, GUARD_DOWN, GUARD_LEFT]
VISITED: str = "X"


def debug_log_grid(grid: list[list[str]]):
    for row in range(0, len(grid[0])):
        logging.debug(f'  {"".join(grid[row])}')
    logging.debug("")


def find_guard(grid: list[list[str]]) -> tuple[int, int] | None:
    for r in range(0, len(grid)):
        for c in range(0, len(grid[r])):
            if grid[r][c] in GUARDS:
                logging.debug(f'Guard found at {(r, c)}')
                return r, c
    return None


def move_guard(grid: list[list[str]], guard_pos: tuple[int, int]) -> tuple[int, int] | None:
    rows = len(grid)
    columns = len(grid[0])

    guard = grid[guard_pos[0]][guard_pos[1]]
    if guard == GUARD_UP:
        offset = [-1, 0]
        next_guard = GUARD_RIGHT
    elif guard == GUARD_RIGHT:
        offset = [0, 1]
        next_guard = GUARD_DOWN
    elif guard == GUARD_DOWN:
        offset = [1, 0]
        next_guard = GUARD_LEFT
    elif guard == GUARD_LEFT:
        offset = [0, -1]
        next_guard = GUARD_UP
    else:
        raise RuntimeError(f'Unexpected guard char {guard} at {guard_pos}')

    for failsafe in range(0, max(rows, columns) + 1):
        grid[guard_pos[0]][guard_pos[1]] = VISITED

        next_pos = (guard_pos[0] + offset[0], guard_pos[1] + offset[1])
        if next_pos[0] not in range(0, rows) or next_pos[1] not in range(0, columns):
            logging.info(f'Guard left grid: last pos {guard_pos} and went {offset}')
            debug_log_grid(grid)
            return None

        next = grid[next_pos[0]][next_pos[1]]
        if next == OBSTACLE:
            grid[guard_pos[0]][guard_pos[1]] = next_guard
            return guard_pos
        elif next == EMPTY or next == VISITED:
            guard_pos = next_pos
            grid[guard_pos[0]][guard_pos[1]] = guard
        else:
            raise RuntimeError(f'Unexpected grid character {next} at {next_pos}')

    raise RuntimeError("Exceeded failsafe for guard!")


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    rows: int = 0
    columns: int = 0
    grid: list[list[str]] = []
    for line in args.input_file[0]:
        line = line.strip()
        if not line:
            continue

        rows += 1
        row = list(line)
        if columns > 0:
            if len(row) != columns:
                logging.error(f'In row {rows}, number of columns changed from {columns} to {len(row)}')
                return 1
        else:
            columns = len(row)
        grid.append(row)

        if args.max_lines > 0 and rows >= args.max_lines:
            logging.warning(f'Halting after {rows} of input per max lines {args.max_lines}')
            break
    logging.debug(f'Read {rows} x {columns} grid')
    debug_log_grid(grid)

    guard_pos = find_guard(grid)
    assert guard_pos, f'Guard not found in grid!'
    failsafe = rows * columns
    while failsafe > 0:
        failsafe -= 1
        guard_pos = move_guard(grid, guard_pos)
        if guard_pos is None:
            break
        logging.debug(f'Guard moved to {guard_pos}')
        #debug_log_grid(grid)
    if failsafe <= 0:
        raise RuntimeError(f'Guard trips exceeded failsafe!')

    assert find_guard(grid) is None, f'Guard is still in grid!'
    visited: int = 0
    for row in grid:
        for col in row:
            if col == VISITED:
                visited += 1
    debug_log_grid(grid)
    logging.info(f'Guard visited {visited} positions')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
