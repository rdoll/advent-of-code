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
    parser.add_argument('-p', '--processes', metavar='#', type=int, default=1,
                        help='number of concurrent processes')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


total_paths_checked: ctypes.c_int = mp.Value(ctypes.c_int, 0)
pending_queue: mp.JoinableQueue = mp.JoinableQueue()
processes: List[mp.Process] = []
process_results: List[ctypes.c_int]

def trace_path(path: str,
               devices: Dict[str, List[str]],
               path_queue: mp.JoinableQueue,
               paths_checked: ctypes.c_int) -> int:
    logger = mp.get_logger()

    pc: int = paths_checked.value + 1
    paths_checked.value = pc
    if pc % 1_000_000 == 0:
        logger.info(f'{pc=:,}')

    device: str = path[-3:]
    if device == 'out':
        if 'dac' in path and 'fft' in path:
            logger.info(f'Found {path=}')
            return 1
        return 0

    for connection in devices[device]:
        if not connection in path:
            path_queue.put(path + ' ' + connection)
    return 0


def worker(process_num: int,
           total_found: ctypes.c_int,
           devices: Dict[str, List[str]],
           path_queue: mp.JoinableQueue,
           paths_checked: ctypes.c_int) -> None:
    logger = mp.get_logger()
    for handler in mp.get_logger().handlers:
        handler.formatter = logging.Formatter('%(asctime)s %(processName)-11s %(levelname)-7s: %(message)s')
    logger.info(f'Started {process_num=}, {total_found=}, {len(devices)=}, {path_queue=}')

    try:
        while True:
            path: str = path_queue.get(block=True, timeout=0.5)
            path_queue.task_done()
            # logger.info(f'{path=}')
            found: int = trace_path(path, devices, path_queue, paths_checked)
            if found > 0:
                logger.info(f'Found {found=}')
                total_found.value += found
    except queue.Empty:
        logger.info(f'Empty queue, {total_found=}')
        return


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

    global pending_queue, processes, process_results
    mp.log_to_stderr(logging.INFO)
    process_results = [mp.Value(ctypes.c_int, 0) for _ in range(args.processes)]
    try:
        for process_num in range(args.processes):
            process: mp.Process = mp.Process(
                target=worker,
                name=f'Process-{process_num:02}',
                args=(process_num, process_results[process_num], devices, pending_queue, total_paths_checked))
            processes.append(process)
            process.start()

        pending_queue.put('svr', block=True, timeout=None)
        pending_queue.join()
        logging.info(f'Queue empty and terminated...')
    except Exception as e:
        logging.error(f'Exception encountered: {e}')
        pending_queue.close()
        sys.exit(-1)

    logging.info(f'Waiting for {args.processes} processes to finish...')
    for p in processes:
        p.join()
    logging.debug(f'{total_paths_checked.value=:,}')

    total: int = sum([p.value for p in process_results])
    logging.info(f'Final {total=}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
