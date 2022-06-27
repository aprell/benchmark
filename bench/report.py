import os

from bench.stats import get_stats, print_csv, print_table


def report(cmd, config, transform=None, tabulate=True):
    print("\n", cmd, f"({config.unit})")
    stats = get_stats(cmd, config)
    if transform:
        stats = transform(stats)
    print_table(stats) if tabulate else print_csv(stats)


def report_all(config, transform=None, tabulate=True):
    for benchmark in config.benchmarks:
        report(benchmark, config, transform, tabulate)
