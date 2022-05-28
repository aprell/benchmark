#!/usr/bin/env python3

import argparse
import os
import statistics
import sys

from bench.utils import get_logfile, get_logfiles, get_run_times


def mean_rsd(numbers):
    """
    Calculate mean and relative standard deviation (RSD) of a series of numbers
    """
    if sys.version_info >= (3,8):
        mean = statistics.fmean(numbers)
    else:
        mean = statistics.mean(numbers)
    try:
        sd = statistics.stdev(numbers)
        rsd = 100 * sd / abs(mean)
    except statistics.StatisticsError:
        # Variance requires at least two data points
        rsd = None
    return mean, rsd


def quartiles(numbers):
    return statistics.quantiles(numbers, n=4, method="inclusive")


def deciles(numbers):
    return statistics.quantiles(numbers, n=10, method="inclusive")


def format_number(n):
    return format_mean_rsd(*n) if isinstance(n, tuple) else \
        str(round(n, 2) if isinstance(n, float) else n)


def format_mean_rsd(mean, rsd):
    return f"{format_number(mean)} ± {format_number(rsd)} %"


def print_csv(stats, file=sys.stdout):
    print(",".join(stats[0]), file=file)
    for i in range(1, len(stats)):
        print(",".join(map(format_number, stats[i])), file=file)
    file.flush()


def print_table(stats, file=sys.stdout):
    import tabulate as T
    for i in range(1, len(stats)):
        stats[i] = map(format_number, stats[i])
    print(T.tabulate(stats, headers="firstrow", tablefmt="pretty"), file=file)
    file.flush()


if sys.version_info >= (3,8):
    headers = [
        "Min", "P10", "P25", "Median", "P75", "P90", "Max",
        "P75-P25", "P90-P10", "Max-Min", "Mean ± RSD"
    ]
else:
    # Fewer stats (no percentiles)
    headers = ["Min", "Median", "Max", "Max-Min", "Mean ± RSD"]


def summarize(numbers):
    if not numbers:
        return []

    if sys.version_info >= (3,8):
        try:
            Q = quartiles(numbers)
            D = deciles(numbers)
        except statistics.StatisticsError:
            # Must have at least two data points
            Q = None
            D = None

        stats = [
            min(numbers),                 # Minimum
            D[0] if D else None,          # 10th percentile / 1st decile
            Q[0] if Q else None,          # 25th percentile / 1st quartile
            Q[1] if Q else None,          # 50th percentile / 2nd quartile / median
            Q[-1] if Q else None,         # 75th percentile / 3rd quartile
            D[-1] if D else None,         # 90th percentile / 9th decile
            max(numbers),                 # Maximum
            Q[-1] - Q[0] if Q else None,  # Interquartile range
            D[-1] - D[0] if D else None,  # Interdecile range
            max(numbers) - min(numbers),  # Total range
            mean_rsd(numbers)             # Mean ± RSD in percent
        ]
    else:
        stats = [
            min(numbers),                 # Minimum
            statistics.median(numbers),   # Median
            max(numbers),                 # Maximum
            max(numbers) - min(numbers),  # Total range
            mean_rsd(numbers)             # Mean ± RSD in percent
        ]

    return stats


def print_stats(numbers, tabulate=True):
    stats = [headers, summarize(numbers)]
    print_table(stats) if tabulate else print_csv(stats)


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--tabulate",
                        action="store_true",
                        help="tabulate output",
                        required=False)

    args = parser.parse_args()

    numbers = []
    for line in sys.stdin:
        numbers.append(float(line))

    print_stats(numbers, args.tabulate)
