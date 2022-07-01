#!/usr/bin/env python3

import argparse

from bench.config import Config
from bench.diff import actual_diff, relative_diff
from bench.metrics import efficiencies, speedups
from bench.plot import plot
from bench.report import report, report_all
from bench.run import run, run_all
from bench.test import test, test_all


def parse_args():
    parser = argparse.ArgumentParser()
    groups = [
        parser.add_mutually_exclusive_group(),
        parser.add_mutually_exclusive_group(),
        parser.add_mutually_exclusive_group(),
        parser.add_mutually_exclusive_group(),
    ]

    groups[0].add_argument("--test",
                           metavar="CMD",
                           nargs="+",
                           help="test benchmarks (discards stdout)",
                           required=False)

    groups[0].add_argument("--test-all",
                           action="store_true",
                           help="test all benchmarks (discards stdout)",
                           required=False)

    groups[1].add_argument("--run",
                           metavar="CMD",
                           nargs="+",
                           help="run benchmarks",
                           required=False)

    groups[1].add_argument("--run-all",
                           action="store_true",
                           help="run all benchmarks",
                           required=False)

    groups[2].add_argument("--report",
                           metavar="CMD",
                           nargs="*",
                           help="report benchmark results",
                           required=False)

    groups[2].add_argument("--report-all",
                           action="store_true",
                           help="report all benchmark results",
                           required=False)

    groups[3].add_argument("--speedup",
                           action="store_const",
                           const=speedups,
                           help="calculate parallel speedups",
                           required=False)

    groups[3].add_argument("--efficiency",
                           action="store_const",
                           const=efficiencies,
                           help="calculate parallel efficiencies",
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

    if args.test:
        for cmd in args.test:
            test(cmd, config)
    elif args.test_all:
        test_all(config)

    if args.run:
        for cmd in args.run:
            run(cmd, config)
    elif args.run_all:
        run_all(config)

    metric = args.speedup or args.efficiency

    if args.report:
        for cmd in args.report:
            report(cmd, config, transform=metric)
    elif args.report == [] and args.run:
        for cmd in args.run:
            report(cmd, config, transform=metric)
    elif args.report_all:
        report_all(config, transform=metric)

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
