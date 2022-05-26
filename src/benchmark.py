#!/usr/bin/env python3

import argparse
import glob
import os
import re
import subprocess

from .stats import print_stats
from .testrun import testrun
from .utils import eprint


def get_num_threads(env):
    """
    Get the value of environment variable `env` if defined, else get the number of CPUs from `lscpu`
    """
    num_threads = os.environ.get(env)
    if not num_threads:
        num_threads = subprocess.check_output("lscpu | grep ^CPU\(s\)", shell=True).split()[1]
    return int(num_threads)


def get_logfile(cmd, suffix=None, ext=None):
    logdir = os.path.join("benchmark.output", os.path.dirname(cmd[0]))
    logfile = os.path.join(logdir, os.path.basename(cmd[0]))
    if len(cmd) > 1:
        logfile += "_" + "_".join(cmd[1:])
    if suffix:
        if type(suffix) == int:
            logfile += f"_{suffix:03}"
        else:
            logfile += f"_{suffix}"
    if ext:
        logfile += f".{ext}"
    return logfile


def get_logfiles(cmd, ext=None):
    def get_num_threads(logfile):
        return int(os.path.splitext(logfile)[0][-3:])
    pattern = get_logfile(cmd) + "*"
    if ext:
        pattern += f".{ext}"
    logfiles = glob.glob(pattern)
    return [(get_num_threads(logfile), logfile) for logfile in sorted(logfiles)]


def get_run_times(logfile):
    run_times = []
    with open(logfile) as file:
        elapsed = re.compile(r"[^:]*: *(\d+(?:\.\d*)?)")
        for line in file:
            match = re.search(elapsed, line)
            if match:
                run_times.append(float(match.group(1)))
    return run_times


def benchmark(cmd, repetitions=10, show_statistics=False, env="OMP_NUM_THREADS"):
    num_threads = get_num_threads(env)
    logfile = get_logfile(cmd, suffix=num_threads, ext="log")
    os.makedirs(os.path.dirname(logfile), exist_ok=True)

    with open(logfile, "w") as file:
        eprint(f"{env}={num_threads} ", end='')
        testrun(cmd, repetitions, stdout=file)

    if show_statistics:
        print_stats(get_run_times(logfile))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--repetitions",
                        type=int, default=10,
                        help="number of repetitions (default is 10)",
                        required=False)

    parser.add_argument("-s", "--show-statistics",
                        action="store_true",
                        help="show summary statistics",
                        required=False)

    parser.add_argument("cmd",
                        nargs="*",
                        help="program to run")

    args = parser.parse_args()

    if args.cmd:
        benchmark(args.cmd, args.repetitions, args.show_statistics)
    else:
        # Read commands from file
        with open("benchmark.input") as file:
            for line in file:
                cmd = line.split()
                benchmark(cmd, args.repetitions, args.show_statistics)
