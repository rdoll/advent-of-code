#!/usr/bin/python3

#
# Advent of Code 2024 Day 11 Part Two
#

import argparse
import functools
import logging
import re
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2024 Day 11 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-b', '--blinks', metavar='#', type=int, default=6,
                        help='blink this many times, 0 = disabled')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


####
#### Basically all of these options are horrible because my part 1 was based on the idea that the order of the stones
#### mattered... which it does not. So carrying around these extra stones just killed performance. Finally swapping
#### to just tracking the total number of stones made this trivial and super fast.
####

# def blink(stone: int, num_blinks: int) -> int:
#     num_stones: int = 1
#     for b in range(0, num_blinks):
#         # Rule 1: If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
#         if stone == 0:
#             stone = 1
#         else:
#             # Rule 2: If the stone is engraved with a number that has an even number of digits, it is replaced by
#             # two stones. The left half of the digits are engraved on the new left stone, and the right half of the
#             # digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000
#             # would become stones 10 and 0.)
#             stone_str = str(stone)
#             if len(stone_str) % 2 == 0:
#                 stone = int(stone_str[:len(stone_str) // 2])
#                 num_stones += blink(int(stone_str[len(stone_str) // 2:]), num_blinks - (b + 1))
#             else:
#                 # Rule 3: If none of the other rules apply, the stone is replaced by a new stone; the old stone's
#                 # number multiplied by 2024 is engraved on the new stone.
#                 stone *= 2024
#     return num_stones


@functools.cache  # reduces 10ish sec loop debug log to 7ish sec
def blink(stone: int, num_blinks: int) -> list[tuple[int, int]]:
    new_stones: list[tuple[int, int]] = []
    for b in range(0, num_blinks):
        # Rule 1: If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        if stone == 0:
            stone = 1
        else:
            # Rule 2: If the stone is engraved with a number that has an even number of digits, it is replaced by
            # two stones. The left half of the digits are engraved on the new left stone, and the right half of the
            # digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000
            # would become stones 10 and 0.)
            stone_str = str(stone)
            if len(stone_str) % 2 == 0:
                stone = int(stone_str[:len(stone_str) // 2])
                new_stones.append( (int(stone_str[len(stone_str) // 2:]), num_blinks - (b + 1)) )
            else:
                # Rule 3: If none of the other rules apply, the stone is replaced by a new stone; the old stone's
                # number multiplied by 2024 is engraved on the new stone.
                stone *= 2024
    return new_stones


def next_blink_with_stones(queue: dict[int, list[int]]) -> int | None:
    for b in sorted(queue.keys()):
        if len(queue[b]) > 0:
            return b
    return None


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')

    stones: list[int] = []
    for line in args.input_file[0]:
        values = re.findall(r"(\d+)", line)
        assert len(values) > 0, f'No stones in line "{line}"'
        [stones.append(int(v)) for v in values]
    logging.info(f'Stones = {stones}')


    total_stones: int = 0
    blinks_remaining: dict[int, list[int]] = {}
    for b in range(0, args.blinks + 1):  # preseed all dict keys
        blinks_remaining[b] = []
    for stone in stones:
        # stones don't affect each other, so do each solo
        logging.info(f'Starting stone {stone}')
        blinks_remaining[args.blinks].append(stone)
        loops: int = 0
        while True:
            blinks = next_blink_with_stones(blinks_remaining)
            if blinks is None:
                break
            for s in blinks_remaining[blinks]:
                loops += 1
                created_stones: list[tuple[int, int]] = blink(s, blinks)
                total_stones += 1
                for created in created_stones:
                    # NB: relying on blink() never returning created with same # of blinks as current for s in ... loop
                    blinks_remaining[created[1]].append(created[0])
                if loops % 5000000 == 0:
                    total_queued: int = sum([len(x) for x in blinks_remaining.values()])
                    logging.debug(f'Stone {stone}, after {loops:,} loops, {total_stones:,} stones, blink_queue {total_queued}')
            blinks_remaining[blinks] = []

        total_queued: int = sum([len(x) for x in blinks_remaining.values()])
        logging.info(f'Stone {stone} complete after {loops:,} loops, {total_stones:,} stones, blink_queue {total_queued}')

    logging.info(f'Total stones {total_stones}')

    # total_stones: int = 0
    # for start_stone in stones:
    #     # stones don't affect each other, so do each solo
    #     loop_stones: list[int] = [start_stone]
    #     for blink in range(0, args.blinks):
    #         new_stones: list[int] = []
    #         for stone in loop_stones:
    #             # Rule 1: If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    #             if stone == 0:
    #                 new_stones.append(1)
    #             else:
    #                 # Rule 2: If the stone is engraved with a number that has an even number of digits, it is replaced by
    #                 # two stones. The left half of the digits are engraved on the new left stone, and the right half of the
    #                 # digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000
    #                 # would become stones 10 and 0.)
    #                 stone_str = str(stone)
    #                 if len(stone_str) % 2 == 0:
    #                     new_stones.append(int(stone_str[:len(stone_str) // 2]))
    #                     new_stones.append(int(stone_str[len(stone_str) // 2:]))
    #                 else:
    #                     # Rule 3: If none of the other rules apply, the stone is replaced by a new stone; the old stone's
    #                     # number multiplied by 2024 is engraved on the new stone.
    #                     new_stones.append(stone * 2024)
    #         loop_stones = new_stones
    #         if (blink + 1) % 10 == 0:
    #             logging.debug(f'Stone {start_stone} completed blink {blink}')
    #
    #     logging.info(f'Stone {start_stone} expanded into {len(loop_stones)} stones after {args.blinks} blinks')
    #     total_stones += len(loop_stones)
    # logging.info(f'Total stones {total_stones}')


    # for blink in range(0, args.blinks):
    #     new_stones: list[str] = []
    #     for stone in stones:
    #         # Rule 1: If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    #         if stone == "0":
    #             new_stones.append("1")
    #         else:
    #             # Rule 2: If the stone is engraved with a number that has an even number of digits, it is replaced by
    #             # two stones. The left half of the digits are engraved on the new left stone, and the right half of the
    #             # digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000
    #             # would become stones 10 and 0.)
    #             if len(stone) % 2 == 0:
    #                 new_stones.append(stone[:len(stone) // 2])
    #                 new_stones.append(stone[len(stone) // 2:])
    #             else:
    #                 # Rule 3: If none of the other rules apply, the stone is replaced by a new stone; the old stone's
    #                 # number multiplied by 2024 is engraved on the new stone.
    #                 new_stones.append(str(int(stone) * 2024))
    #     stones = new_stones
    #
    #     logging.info(f'After {blink + 1} blinks, {len(stones)} stones = {stones[:50]}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
