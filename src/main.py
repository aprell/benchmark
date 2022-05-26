#!/usr/bin/env python3

import argparse
import configparser
import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from src.benchmark import benchmark, get_logfile, get_logfiles, get_run_times
from src.stats import headers, print_csv, print_table, summarize
from src.utils import GREEN as GOOD, RED as BAD, RESET


class BenchmarkConfig:
    @classmethod
    def read_list(_, lst, type=str):
        return [type(x.strip()) for x in lst.split(",")]

    def __init__(self, configfile):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

        self.benchmarks = BenchmarkConfig.read_list(self.config.get("Benchmark", "benchmarks"))
        self.runtimes = BenchmarkConfig.read_list(self.config.get("Benchmark", "runtimes"))
        self.num_threads = self.config.get("Benchmark", "num_threads")

        self.environment = {}
        for var, value in self.config["Environment"].items():
            self.environment[var.upper()] = value

        assert(self.num_threads in self.environment)
        self.environment[self.num_threads] = BenchmarkConfig.read_list(self.environment[self.num_threads], type=int)

    def print(self):
        print("[Benchmark]")
        print("benchmarks =", self.benchmarks)
        print("runtimes =", self.runtimes)
        print("num_threads =", self.num_threads)
        print("\n[Environment]")
        for k, v in self.environment.items():
            print(k, "=", v)


def transform(func):
    def apply(stats, base=None):
        # Remove column headers and last four columns
        headers = stats[0][:-4]
        numbers = np.array(stats)[1:,:-4].astype(float)
        # Add back column headers
        return [headers] + func(numbers)
    return apply


@transform
def speedups(numbers, base=None):
    base = base if base else numbers[0][4]
    return [[int(n), *reversed([base/x for x in xs])] for n, *xs in numbers]


@transform
def efficiencies(numbers, base=None):
    base = base if base else numbers[0][4]
    return [[int(n), *reversed([base/x/n for x in xs])] for n, *xs in numbers]


def run(cmd, config):
    os.environ.update({
        k: v for k, v in config.environment.items()
        if k != config.num_threads})

    cmd = cmd.split()

    for n in config.environment[config.num_threads]:
        os.environ[config.num_threads] = str(n)
        benchmark(cmd, env=config.num_threads)

    csv_file = get_logfile(cmd, ext="csv")
    if os.path.exists(csv_file):
        os.remove(csv_file)


def run_all(config):
    for benchmark in config.benchmarks:
        for runtime in config.runtimes:
            run(os.path.join(runtime, benchmark), config)


def get_stats(cmd):
    cmd = cmd.split()
    csv_file = get_logfile(cmd, ext="csv")
    if not os.path.exists(csv_file):
        with open(csv_file, "w") as file:
            stats = [["#Threads"] + headers]
            for n, logfile in get_logfiles(cmd, ext="log"):
                stats.append([n] + summarize(get_run_times(logfile)))
            print_csv(stats, file=file)
    else:
        with open(csv_file, "r") as file:
            stats = []
            for line in file:
                stats.append(line.strip().split(","))
    return stats


def report(cmd, transform=None, tabulate=True):
    print("\n", cmd)
    stats = get_stats(cmd)
    if transform:
        stats = transform(stats)
    print_table(stats) if tabulate else print_csv(stats)


def report_all(config, transform=None, tabulate=True):
    for benchmark in config.benchmarks:
        for runtime in config.runtimes:
            report(os.path.join(runtime, benchmark), transform, tabulate)


def plot(cmds, outfile, xlabel="Number of threads", ylabel="Median run times (ms)", transform=None):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    for cmd in cmds:
        stats = get_stats(cmd)
        if transform:
            stats = transform(stats)
        # Remove column headers
        stats = np.array(stats[1:])

        num_threads = stats[:,0].astype(int)
        median_values = stats[:,4].astype(float)
        lower_errors = median_values - stats[:,2].astype(float)
        upper_errors = stats[:,6].astype(float) - median_values

        plt.errorbar(num_threads,
                     median_values,
                     yerr=[lower_errors, upper_errors],
                     label=os.path.dirname(cmd).upper())

    plt.legend()
    plt.savefig(outfile)


def format_number(n, suffix=""):
    return f"{BAD}+{n:.2f}{suffix}{RESET}" if n > 0 else f"{GOOD}{n:.2f}{suffix}{RESET}"


def actual_diff(a, b):
    return np.vectorize(lambda n: format_number(n, suffix=" ms"))(a - b)


def relative_diff(a, b):
    return np.vectorize(lambda n: format_number(n, suffix=" %"))((a - b) / b * 100)


def diff(cmds, func):
    a = np.array(get_stats(cmds[0]))
    b = np.array(get_stats(cmds[1]))
    d = func(a[1:,1:-4].astype(float), b[1:,1:-4].astype(float))
    print("\n", cmds[0], "vs", cmds[1])
    print_table(np.r_[[a[0,:-4]], np.c_[a[1:,0], d]].tolist())


def main():
    parser = argparse.ArgumentParser()
    run_group = parser.add_mutually_exclusive_group()
    rep_group = parser.add_mutually_exclusive_group()
    fun_group = parser.add_mutually_exclusive_group()

    run_group.add_argument("--run",
                           metavar="CMD",
                           nargs="+",
                           help="run benchmarks",
                           required=False)

    run_group.add_argument("--run-all",
                           action="store_true",
                           help="run all benchmarks",
                           required=False)

    rep_group.add_argument("--report",
                           metavar="CMD",
                           nargs="*",
                           help="report benchmark results",
                           required=False)

    rep_group.add_argument("--report-all",
                           action="store_true",
                           help="report all benchmark results",
                           required=False)

    fun_group.add_argument("--speedup",
                           action="store_const",
                           const=speedups,
                           help="calculate parallel speedups",
                           required=False)

    fun_group.add_argument("--efficiency",
                           action="store_const",
                           const=efficiencies,
                           help="calculate parallel efficiencies",
                           required=False)

    parser.add_argument("--plot",
                        metavar="CMD",
                        nargs="+",
                        help="plot benchmark results",
                        required=False)

    parser.add_argument("-o", "--output",
                        metavar="FILE",
                        help="save figure as file",
                        required=False)

    parser.add_argument("--diff",
                        metavar="CMD",
                        nargs=2,
                        help="show difference between two benchmark results",
                        required=False)

    args = parser.parse_args()

    if args.output and not args.plot:
        parser.error("argument -o/--output requires --plot")

    config = BenchmarkConfig("bench.cfg")

    if args.run:
        for cmd in args.run:
            run(cmd, config)
    elif args.run_all:
        run_all(config)

    func = args.speedup or args.efficiency

    if args.report:
        for cmd in args.report:
            report(cmd, transform=func)
    elif args.report == [] and args.run:
        for cmd in args.run:
            report(cmd, transform=func)
    elif args.report_all:
        report_all(config, transform=func)

    if args.plot:
        outfile = args.output if args.output else "plot.png"
        if args.speedup:
            plot(args.plot, outfile, ylabel="Median speedups", transform=func)
        elif args.efficiency:
            plot(args.plot, outfile, ylabel="Median efficiencies", transform=func)
        else:
            # Median run times
            plot(args.plot, outfile)

    if args.diff:
        diff(args.diff, func=actual_diff)
        diff(args.diff, func=relative_diff)


if __name__ == "__main__":
    main()
