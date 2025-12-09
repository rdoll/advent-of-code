#!/usr/bin/python3

import argparse
import logging
import sys
from typing import List

import numpy as np
import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 08 Part 1 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')
    parser.add_argument('-t', '--top', default='10', type=int, help='top n closet junction boxes')

    args = parser.parse_args()
    return args


def calculate_distances(in_df: pd.DataFrame) -> pd.DataFrame:
    boxes: int = in_df.shape[0]
    dist_df = pd.DataFrame(np.full([boxes, boxes], np.inf, dtype=float))

    for row1 in range(0, boxes - 1):
        for row2 in range(row1 + 1, boxes):
            dist_df.iat[row1, row2] = np.linalg.norm(in_df.iloc[row1, :] - in_df.iloc[row2, :])

    return dist_df


def top_closest_distances(in_df: pd.DataFrame, dist_df: pd.DataFrame, top_n: int) -> pd.DataFrame:
    top_df: pd.DataFrame = pd.DataFrame(dtype=float, columns=['distance', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2'])

    (_, cols) = dist_df.shape
    for i in range(0, top_n):
        flat_idx: int = np.argmin(dist_df.to_numpy()).item()
        min_dist_row: int = flat_idx // cols
        min_dist_col: int = flat_idx % cols
        min_dist: float = dist_df.iat[min_dist_row, min_dist_col]
        top_df.loc[len(top_df)] = [min_dist,
            in_df.loc[min_dist_row, 0], in_df.loc[min_dist_row, 1], in_df.loc[min_dist_row, 2],
            in_df.loc[min_dist_col, 0], in_df.loc[min_dist_col, 1], in_df.loc[min_dist_col, 2]]
        dist_df.iat[min_dist_row, min_dist_col] = np.inf

    return top_df


class Circuit:
    boxes: List[np.ndarray]

    def __init__(self):
        self.boxes = []

    def has_box(self, box: np.ndarray) -> bool:
        for circuit_box in self.boxes:
            if np.all(circuit_box == box):
                return True
        return False

    def overlaps_circuit(self, other: 'Circuit') -> bool:
        for self_box in self.boxes:
            if other.has_box(self_box):
                return True
        for other_box in other.boxes:
            if self.has_box(other_box):
                return True
        return False

    def add_box(self, box: np.ndarray) -> None:
        if not self.has_box(box):
            self.boxes.append(box)

    def add_circuit(self, other: 'Circuit') -> None:
        for other_box in other.boxes:
            self.add_box(other_box)

    def size(self) -> int:
        return len(self.boxes)

    def __repr__(self) -> str:
        s: str = f'boxes={len(self.boxes)}: '
        s += ' => '.join([f'{box[0]},{box[1]},{box[2]}' for box in self.boxes])
        return s


def build_circuits(closest_distances: pd.DataFrame) -> List[Circuit]:
    circuits: List[Circuit] = []

    for row_series in closest_distances.itertuples():
        box1: np.ndarray = np.array([row_series.x1, row_series.y1, row_series.z1])
        box2: np.ndarray = np.array([row_series.x2, row_series.y2, row_series.z2])

        added: bool = False
        for circuit in circuits:
            if circuit.has_box(box1) or circuit.has_box(box2):
                circuit.add_box(box1)
                circuit.add_box(box2)
                added = True
                break

        if not added:
            circuit: Circuit = Circuit()
            circuit.add_box(box1)
            circuit.add_box(box2)
            circuits.append(circuit)

    return circuits


def combine_circuits(circuits: List[Circuit]) -> List[Circuit]:
    combined_circuits: List[Circuit] = list(circuits)
    uncombined_circuits: List[Circuit]

    # dumbly repeat so each circuit can be combined with multiple other circuits
    for i in range(0, len(circuits)):
        uncombined_circuits = combined_circuits
        combined_circuits = []
        initial_count: int = len(uncombined_circuits)

        while len(uncombined_circuits) > 0:
            uncombined: Circuit = uncombined_circuits.pop(0)
            did_combine: bool = False
            for combined in combined_circuits:
                if combined.overlaps_circuit(uncombined):
                    combined.add_circuit(uncombined)
                    did_combine = True
                    break
            if not did_combine:
                combined_circuits.append(uncombined)

        if len(combined_circuits) == initial_count:
            break
        else:
            logging.debug(f'combined {initial_count - len(combined_circuits)}, {initial_count=}, {len(combined_circuits)=}')

    logging.info(f'finished combining {len(circuits)} circuits into {len(combined_circuits)} circuits')
    return combined_circuits


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    in_df: pd.DataFrame  = pd.read_table(args.input_file[0], sep=r',', header=None, comment=';')
    logging.info(f'{in_df.shape=}')

    dist_df: pd.DataFrame = calculate_distances(in_df)
    logging.info(f'{dist_df.shape=}')
    logging.debug(f'dist_df=\n{dist_df}')

    closest_distances: pd.DataFrame = top_closest_distances(in_df, dist_df, args.top)
    logging.info(f'{args.top=}, closest_distances=\n{closest_distances}')

    uncombined_circuits: List[Circuit] = build_circuits(closest_distances)
    logging.info(f'uncombined_circuits=[\n{"\n".join([str(c) for c in uncombined_circuits])}]')

    combined_circuits: List[Circuit] = combine_circuits(uncombined_circuits)
    combined_circuits.sort(key=lambda circuit: circuit.size(), reverse=True)
    logging.info(f'combined_circuits=[\n{"\n".join([str(c) for c in combined_circuits])}]')

    largest_circuits_total: int = (
        combined_circuits[0].size() * combined_circuits[1].size() * combined_circuits[2].size())
    logging.info(f'Final {largest_circuits_total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
