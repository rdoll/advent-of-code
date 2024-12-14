#!/usr/bin/python3

#
# Advent of Code 2024 Day 13 Part Two
#

import argparse
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 13 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class ClawMachine:
    TOKENS_PER_A: int = 3
    TOKENS_PER_B: int = 1
    PRIZE_OFFSET: int = 10_000_000_000_000

    def __init__(self, ax: int, ay: int, bx: int, by: int, px: int, py: int):
        self.ax: int = ax
        self.ay: int = ay
        self.bx: int = bx
        self.by: int = by
        self.px: int = px + ClawMachine.PRIZE_OFFSET
        self.py: int = py + ClawMachine.PRIZE_OFFSET

    def __str__(self):
        return (f'button A = {self.ax} x {self.ay}, button B = {self.bx} x {self.by}, prize = {self.px} x {self.py}')

    def find_min_tokens(self) -> int | None:
        num_bs_denom: int = (self.by * self.ax) - (self.bx * self.ay)
        if num_bs_denom == 0:
            logging.debug(f'num_bs_denom = 0 for {self}')
            return None

        num_bs: int = ((self.py * self.ax) - (self.ay * self.px)) // num_bs_denom
        num_as: int = (self.px - (num_bs * self.bx)) // self.ax
        claw_x: int = (num_as * self.ax) + (num_bs * self.bx)
        claw_y: int = (num_as * self.ay) + (num_bs * self.by)
        if claw_x != self.px or claw_y != self.py:
            # fractions of a button press are required to reach the prize
            logging.debug(f'No prize for {self}')
            return None

        tokens: int = (num_as * ClawMachine.TOKENS_PER_A) + (num_bs * ClawMachine.TOKENS_PER_B)
        logging.debug(f'Prize with {num_as} As and {num_bs} Bs for {tokens} tokens on machine {self}')
        return tokens


def load_claw_machines(input_file) -> list[ClawMachine]:
    claw_machines: list[ClawMachine] = []
    ax: int | None = None
    ay: int | None = None
    bx: int | None = None
    by: int | None = None
    for line in input_file:
        line = line.strip()
        if not line:
            continue

        if re.match(r'^\s*Button\s+A', line):
            assert ax == None and ay == None, f'Already have an ax and/or ay!'
            assert ax != 0 and ay != 0, f'ax and/or ay cannot be zero!'
            [ax, ay] = [int(n) for n in list(re.findall(r'X\+(\d+), Y\+(\d+)', line)[0])]
        elif re.match(r'^\s*Button\s+B', line):
            assert bx == None and by == None, f'Already have a bx and/or by!'
            assert bx != 0 and by != 0, f'bx and/or by cannot be zero!'
            [bx, by] = [int(n) for n in list(re.findall(r'X\+(\d+), Y\+(\d+)', line)[0])]
        elif re.match(r'^\s*Prize', line):
            assert ax != None and ay != None and bx != None and by != None, f'Prize missing buttons!'
            [px, py] = [int(n) for n in list(re.findall(r'X=(\d+), Y=(\d+)', line)[0])]
            assert px != 0 and py != 0, f'Cannot handle prize at claw origin!'
            claw_machine: ClawMachine = ClawMachine(ax, ay, bx, by, px, py)
            claw_machines.append(claw_machine)
            logging.debug(f'Loaded claw machine: {claw_machine}')
            ax = ay = bx = by = None
        else:
            raise RuntimeError(f'Unknown line {line}')

    return claw_machines


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    claw_machines: list[ClawMachine] = load_claw_machines(args.input_file[0])
    logging.info(f'Loaded {len(claw_machines)} claw machines')

    num_prizes: int = 0
    total_tokens: int = 0
    for claw_machine in claw_machines:
        min_tokens: int | None = claw_machine.find_min_tokens()
        if min_tokens is None:
            logging.info(f'No prize for claw machine: {claw_machine}')
        else:
            logging.info(f'Prize with {min_tokens} for claw machine: {claw_machine}')
            num_prizes += 1
            total_tokens += min_tokens

    logging.info(f'Can spend {total_tokens} tokens to get {num_prizes} prizes from {len(claw_machines)} machines')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
