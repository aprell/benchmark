import os
import subprocess

from bench.args import add_argument
from bench.utils import run as test_run


def test(cmd, config):
    cmd = cmd.split()
    test_run(cmd, config.repetitions, stdout=subprocess.DEVNULL)


def setup(subparsers):
    parser = subparsers.add_parser("test", help="test benchmarks (discards stdout)")
    parser.add_argument("cmds", metavar="CMD", nargs="*")
    add_argument(parser, "--all")

    parser.set_defaults(run=main)


def main(args, config):
    for cmd in args.all and config.benchmarks or args.cmds:
        test(cmd, config)
