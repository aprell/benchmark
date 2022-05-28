#!/usr/bin/env python3

import argparse

from bench.config import Config
from bench.diff import actual_diff, diff, relative_diff
from bench.metrics import efficiencies, speedups
from bench.plot import plot
from bench.report import report, report_all
from bench.run import run, run_all
from bench.test import test, test_all


def parse_args():
    parser = argparse.ArgumentParser()
    tst_group = parser.add_mutually_exclusive_group()
    run_group = parser.add_mutually_exclusive_group()
    rep_group = parser.add_mutually_exclusive_group()
    fun_group = parser.add_mutually_exclusive_group()

    tst_group.add_argument("--test",
                           metavar="CMD",
                           nargs="+",
                           help="test benchmarks (discards stdout)",
                           required=False)

    tst_group.add_argument("--test-all",
                           action="store_true",
                           help="test all benchmarks (discards stdout)",
                           required=False)

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

    return args


def main():
    args = parse_args()
    config = Config("bench.cfg")

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
        diff(args.diff, func=actual_diff, unit="ms")
        diff(args.diff, func=relative_diff, unit="%")


if __name__ == "__main__":
    main()