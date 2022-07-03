#!/usr/bin/env python3

import argparse

from bench.config import Config
from bench.diff import actual_diff, relative_diff
from bench.metrics import efficiencies, speedups
from bench.plot import plot
from bench.report import report
from bench.run import run
from bench.test import test


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--test",
                        metavar="CMD",
                        nargs="*",
                        help="test benchmarks (discards stdout)",
                        required=False)

    parser.add_argument("--run",
                        metavar="CMD",
                        nargs="*",
                        help="run benchmarks",
                        required=False)

    parser.add_argument("--report",
                        metavar="CMD",
                        nargs="*",
                        help="report benchmark results",
                        required=False)

    parser.add_argument("--all",
                        action="store_true",
                        help="consider all benchmarks in configuration file",
                        required=False)

    parser.add_argument("--diff",
                        metavar="CMD",
                        nargs=2,
                        help="show difference between two benchmark results",
                        required=False)

    parser.add_argument("--actual",
                        action="store_true",
                        help="show actual difference",
                        required=False)

    parser.add_argument("--relative",
                        action="store_true",
                        help="show relative difference in percent",
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

    metrics = parser.add_mutually_exclusive_group()

    metrics.add_argument("--speedup",
                         action="store_const",
                         const=speedups,
                         help="calculate parallel speedups",
                         required=False)

    metrics.add_argument("--efficiency",
                         action="store_const",
                         const=efficiencies,
                         help="calculate parallel efficiencies",
                         required=False)

    args = parser.parse_args()

    if args.actual and not args.diff:
        parser.error("argument --actual requires --diff")

    if args.relative and not args.diff:
        parser.error("argument --relative requires --diff")

    if args.output and not args.plot:
        parser.error("argument -o/--output requires --plot")

    return args


def main():
    args = parse_args()
    config = Config("bench.ini")

    if args.test or args.test == []:
        for cmd in args.all and config.benchmarks or args.test:
            test(cmd, config)

    if args.run or args.run == []:
        for cmd in args.all and config.benchmarks or args.run:
            run(cmd, config)

    metric = args.speedup or args.efficiency

    if args.report or args.report == []:
        for cmd in args.all and config.benchmarks or args.report or args.run:
            report(cmd, config, transform=metric)

    if args.diff:
        if args.actual and not args.relative:
            actual_diff(args.diff, config)
        elif args.relative and not args.actual:
            relative_diff(args.diff, config)
        else:
            actual_diff(args.diff, config)
            relative_diff(args.diff, config)

    if args.plot:
        outfile = args.output if args.output else "plot.png"
        if args.speedup:
            plot(args.plot, config, outfile, ylabel="Median speedups", transform=metric)
        elif args.efficiency:
            plot(args.plot, config, outfile, ylabel="Median efficiencies", transform=metric)
        else:
            plot(args.plot, config, outfile, ylabel=f"Median run times ({config.unit})")


if __name__ == "__main__":
    main()
