#!/usr/bin/python3

import argparse
import ctypes
import logging
import multiprocessing as mp
import queue
import re
import sys
from typing import List, Dict


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 11 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-p', '--processes', metavar='#', type=int, default=2,
                        help='number of concurrent processes')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


class Worker:
    work_queue: mp.JoinableQueue
    results: ctypes.c_int
    devices: Dict[str, List[str]]
    paths_checked: int
    found: int
    max_depth: int
    num_events: int

    def __init__(self,
                 work_queue: mp.JoinableQueue,
                 results: ctypes.c_int,
                 devices: Dict[str, List[str]]) -> None:
        self.work_queue = work_queue
        self.results = results
        self.devices = devices
        self.paths_checked = 0
        self.found = 0
        self.max_depth = 0
        self.num_events = 0

    def __repr__(self):
        return (f'Worker(results.value={self.results.value}, #devices={len(self.devices)}'
            f', paths_checked={self.paths_checked}, found={self.found}, max_depth={self.max_depth}'
            f', num_events={self.num_events})')

    def trace_path(self, path: str, depth: int) -> int:
        if depth > self.max_depth:
            self.max_depth = depth

        self.paths_checked += 1
        if self.paths_checked % 500_000 == 0:
            mp.get_logger().info(f'{self.paths_checked=:,}, {self.max_depth=}, {self.num_events=}')

        device: str = path[-3:]
        if device == 'out':
            if 'dac' in path and 'fft' in path:
                mp.get_logger().info(f'Found {path=}')
                return 1
            return 0

        found: int = 0
        for connection in self.devices[device]:
            if not connection in path:
                next_path: str = f'{path} {connection}'
                if depth > 10 and depth % 5 == 0:
                    self.work_queue.put(next_path)
                else:
                    found += self.trace_path(next_path, depth + 1)
        return found

    def start(self) -> None:
        mp.get_logger().info(f'Starting {self}')

        try:
            while True:
                path: str = self.work_queue.get(block=True, timeout=0.5)
                self.work_queue.task_done()
                self.num_events += 1
                depth: int =  ((len(path) - 3) // 4) + 1
                # mp.get_logger().info(f'Dequeued {path=}, {depth=}')
                found: int = self.trace_path(path, depth)
                if found > 0:
                    self.found += found
                    mp.get_logger().info(f'Found {found=}, {self.found=}')
        except queue.Empty:
            self.results.value = self.found
            mp.get_logger().info(f'Empty queue, final state {self}')


def configure_logger_format(logger: logging.Logger) -> None:
    for handler in logger.handlers:
        handler.formatter = logging.Formatter('%(asctime)s %(processName)-11s %(levelname)-7s: %(message)s')


def start_worker(work_queue: mp.JoinableQueue, results: ctypes.c_int, devices: Dict[str, List[str]]) -> None:
    configure_logger_format(mp.get_logger())
    worker: Worker = Worker(work_queue, results, devices)
    worker.start()


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(processName)-10s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    devices: Dict[str, List[str]] = {}
    for line in args.input_file[0]:
        match: re.Match = re.match(r'^\s*(\S+):\s*(.*)\s*$', line.strip())
        if not match:
            logging.warning(f'Skipping invalid {line=}')
            continue
        device: str = match.group(1)
        connections: List[str] = match.group(2).split()
        devices[device] = connections
    logging.debug(f'Found {len(devices)} {devices=}')

    mp.log_to_stderr(logging.INFO)
    configure_logger_format(mp.get_logger())

    work_queue: mp.JoinableQueue = mp.JoinableQueue()
    processes: List[mp.Process] = []
    process_results: List[ctypes.c_int] = [mp.Value(ctypes.c_int, 0) for _ in range(args.processes)]
    try:
        work_queue.put('svr')
        for process_num in range(args.processes):
            process: mp.Process = mp.Process(target=start_worker,
                                             name=f'Process-{process_num:02}',
                                             args=(work_queue, process_results[process_num], devices))
            processes.append(process)
            process.start()
    except Exception as e:
        logging.error(f'Exception encountered: {e}')
        work_queue.close()
        for process in processes:
            process.close()
        sys.exit(-1)

    logging.info(f'Waiting for {args.processes} processes to finish...')
    for p in processes:
        p.join()

    total: int = sum([p.value for p in process_results])
    logging.info(f'Final {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
