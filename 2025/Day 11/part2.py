#!/usr/bin/python3

import argparse
import logging
import queue
import re
import sys
import threading
from queue import Queue
from threading import Thread
from typing import List, Dict, Tuple


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='Advent of Code 2025 Day 11 Part 2 Solution')

    parser.add_argument('-d', '--debug', action='store_true', help='show debug logs')
    parser.add_argument('-t', '--threads', metavar='#', type=int, default=1,
                        help='number of concurrent threads')
    parser.add_argument('input_file', metavar="input-file", nargs=1, type=argparse.FileType('r'),
                        help='input file')

    args = parser.parse_args()
    return args


total_paths_checked: int = 0
devices: Dict[str, List[str]] = {}

pending_queue: Queue[str] = Queue()
threads: List[Tuple[Thread, int]] = []

def trace_path(path: str) -> int:
    global total_paths_checked
    total_paths_checked += 1
    if total_paths_checked % 10_000_000 == 0:
        logging.debug(f'{total_paths_checked=:,}')

    global devices
    device: str = path[-3:]
    if device == 'out':
        if 'dac' in path and 'fft' in path:
            logging.debug(f'Found {path=}')
            return 1
        return 0

    for connection in devices[device]:
        if not connection in path:
            global pending_queue
            pending_queue.put(path + ' ' + connection)
    return 0


def worker(thread_num: int) -> None:
    global pending_queue
    while True:
        try:
            path: str = pending_queue.get(block=True, timeout=2)
            print(f'worker: {path=}')
            found: int = trace_path(path)
            if found > 0:
                global threads
                threads[thread_num][1] += found
            pending_queue.task_done()
        except queue.Empty:
            logging.info(f'{threading.current_thread().name} empty queue')


def main() -> int:
    args = parse_args()
    logging.basicConfig(format='%(asctime)s %(levelname)-7s: %(message)s',
                        level=logging.DEBUG if args.debug else logging.INFO)
    logging.info(f'Starting {sys.argv[0]} to read {args.input_file[0].name}...')
    logging.debug(f'{args=}')

    global devices
    for line in args.input_file[0]:
        match: re.Match = re.match(r'^\s*(\S+):\s*(.*)\s*$', line.strip())
        if not match:
            logging.warning(f'Skipping invalid {line=}')
            continue
        device: str = match.group(1)
        connections: List[str] = match.group(2).split()
        devices[device] = connections
    logging.debug(f'Found {len(devices)} {devices=}')

    global threads
    for thread_num in range(args.threads):
        thread: Thread = Thread(target=trace_path, name=f'Thread-{thread_num:02}', args=[thread_num])
        threads.append((thread, 0))
        thread.start()

    global pending_queue
    pending_queue.put('svr')
    pending_queue.join()
    logging.info(f'Queue empty and terminated...')

    total: int = sum([t[1] for t in threads])
    logging.info(f'Final total: {total=}')
    logging.debug(f'{total_paths_checked=:,}')

    logging.info('Completed successfully')
    return 0


if __name__ == '__main__':
    sys.exit(main())
