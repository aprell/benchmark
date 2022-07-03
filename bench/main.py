#!/usr/bin/env python3

import argparse

from bench import config, diff, plot, report, run, test


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    test.setup(subparsers)
    run.setup(subparsers)
    report.setup(subparsers)
    diff.setup(subparsers)
    plot.setup(subparsers)

    args = parser.parse_args()
    args.run(args, config.Config("bench.ini"))


if __name__ == "__main__":
    main()
