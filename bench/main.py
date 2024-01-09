#!/usr/bin/env python3

import argparse

from bench import config, diff, plot, report, run, test


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", metavar="FILE", help="use FILE as config file", required=False)
    subparsers = parser.add_subparsers()

    for cmd in [test, run, report, diff, plot]:
        cmd.setup(subparsers)

    args = parser.parse_args()
    args.run(args, config.Config(args.file or "bench.ini"))


if __name__ == "__main__":
    main()
