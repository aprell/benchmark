import os

from bench.args import common
from bench.stats import get_stats, print_csv, print_table


def report(cmd, config, transform=None, tabulate=True):
    print("\n", cmd, f"({config.unit})")
    stats = get_stats(cmd, config)
    if transform:
        stats = transform(stats)
    print_table(stats) if tabulate else print_csv(stats)


def setup(subparsers):
    parser = subparsers.add_parser("report", help="report benchmark results")
    parser.add_argument("cmds", metavar="CMD", nargs="*")
    parser.add_argument("--all", **common["--all"])

    metrics = parser.add_mutually_exclusive_group()
    metrics.add_argument("--speedup", **common["--speedup"])
    metrics.add_argument("--efficiency", **common["--efficiency"])

    parser.set_defaults(run=main)


def main(args, config):
    metric = args.speedup or args.efficiency
    for cmd in args.all and config.benchmarks or args.cmds:
        report(cmd, config, transform=metric)
