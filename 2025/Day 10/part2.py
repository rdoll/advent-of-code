#!/usr/bin/python3

import argparse
import logging
import re
import sys
from copy import deepcopy
from typing import List


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 10 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Button:
    MAX_BUTTONS: int = 13
    MASK_STR_WIDTH: int = 13 + 13 // 4
    # MAX_BUTTONS: int = 6
    # MASK_STR_WIDTH: int = 6 + 6 // 4
    mask: int

    def __init__(self, mask: int | List[str]) -> None:
        assert mask is not None
        if isinstance(mask, list):
            mask = Button.to_int(mask)
        assert mask > 0
        self.mask = mask

    def __repr__(self) -> str:
        return Button.to_str(self.mask)

    @staticmethod
    def to_str(mask: int) -> str:
        bit_nums: List[str] = []
        for bit_num in range(0, Button.MAX_BUTTONS):
            if mask & (1 << bit_num) > 0:
                bit_nums.append(str(bit_num))
        return f'({",".join(bit_nums)})={mask:0{Button.MASK_STR_WIDTH}_b}'

    @staticmethod
    def to_int(light_nums: List[str]) -> int:
        mask: int = 0
        for bit_num in light_nums:
            mask += 1 << int(bit_num)
        return mask


class LightPanel:
    MAX_LIGHTS: int = 12
    LIGHT_ON: str = '#'
    LIGHT_OFF: str = '.'
    panel: int
    size: int

    def __init__(self, lights: str) -> None:
        assert lights is not None and len(lights) > 0
        self.size = len(lights)
        self.panel = LightPanel.to_int(lights)

    def __repr__(self) -> str:
        return LightPanel.to_str(self.panel, self.size)

    @staticmethod
    def to_str(panel: int, size: int) -> str:
        lights: str = ''
        for i in range(0, size):
            lights += LightPanel.LIGHT_ON if panel % 2 == 1 else LightPanel.LIGHT_OFF
            panel >>= 1
        return f'[{lights}]'

    @staticmethod
    def to_int(lights: str) -> int:
        panel: int = 0
        for c in list(lights[::-1]):
            panel <<= 1
            if c == LightPanel.LIGHT_ON:
                panel += 1
            elif c == LightPanel.LIGHT_OFF:
                panel += 0
            else:
                raise ValueError(f'Unknown light symbol {c=}, {lights=}')
        return panel


class ButtonCombo:
    button_masks: List[int]
    panel: int

    def __init__(self) -> None:
        self.button_masks = []
        self.panel = 0

    def __repr__(self) -> str:
        button_masks: str = ','.join([Button.to_str(bm) for bm in self.button_masks])
        return f'panel={self.panel}, button_masks=[{button_masks}]'

    # f'{i=:04b}, {b=:04b}, {i & ~b=:04b}, {~i & b=:04b}, {(i & ~b) | ((i & b) ^ b)=:04b}, {(i & ~b) | (~i & b)=:04b}'
    # 'i=1010, b=0011, i & ~b=1000, ~i & b=0001, (i & ~b) | ((i & b) ^ b)=1001, (i & ~b) | (~i & b)=1001'
    def press(self, button_mask: int) -> int:
        self.panel = (self.panel & ~button_mask) | (~self.panel & button_mask)
        self.button_masks.append(button_mask)
        return self.panel


class Machine:
    target_panel: LightPanel
    buttons: List[Button]
    joltages: List[int]

    def __init__(self, target_lights: str, buttons: List[Button], joltages: List[int]) -> None:
        assert target_lights is not None and len(target_lights) > 0
        assert buttons is not None and len(buttons) > 0
        assert joltages is not None and len(joltages) > 0
        self.target_panel = LightPanel(target_lights)
        self.buttons = buttons
        self.joltages = joltages

    def __repr__(self) -> str:
        buttons: List[str] = [str(b) for b in self.buttons]
        joltages: List[str] = [str(j) for j in self.joltages]
        return f'[{self.target_panel}] {" ".join(buttons)} {{{",".join(joltages)}}}'

    def activate(self) -> ButtonCombo:
        pending_combos: List[ButtonCombo] = [ButtonCombo()]
        for failsafe in range(0, Button.MAX_BUTTONS):
            next_pending_combos: List[ButtonCombo] = []

            while len(pending_combos) > 0:
                combo: ButtonCombo = pending_combos.pop(0)
                for button in self.buttons:
                    if len(combo.button_masks) > 0 and button.mask == combo.button_masks[-1]:
                        continue  # No value in pressing same button twice in a row
                    new_combo: ButtonCombo = deepcopy(combo)
                    if new_combo.press(button.mask) == self.target_panel.panel:
                        return new_combo
                    next_pending_combos.append(new_combo)

            pending_combos = next_pending_combos

        raise RuntimeError(f'Failed to find combo for {self=}')


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    machines: List[Machine] = []
    for line in args.input_file[0]:
        match: re.Match = re.match(r'^\s*\[([#.]+)]\s+([0-9, ()]+)\s+\{([0-9,]+)}$', line.strip())
        if not match:
            logging.warning(f'Skipping invalid {line=}')
            continue

        lights: str = match.group(1)
        buttons: List[Button] = []
        for button_lights in match.group(2).split(' '):
            buttons.append(Button([light_num for light_num in button_lights.lstrip('(').rstrip(')').split(',')]))
        joltages: List[int] = [int(j) for j in match.group(3).split(',')]
        machine: Machine = Machine(lights, buttons, joltages)
        machines.append(machine)
        logging.debug(f'Read {machine=}')

    total: int = 0
    for machine in machines:
        combo: ButtonCombo = machine.activate()
        logging.info(f'Used {len(combo.button_masks)} in {combo} for {machine}')
        total += len(combo.button_masks)
    logging.info(f'Final total: {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
