#!/usr/bin/env python3

import argparse
import subprocess

from .utils import BOLD, RED, RESET
from .utils import eprint


def testrun(cmd, repetitions=10, stdout=None, stderr=None):
    eprint(" ".join(cmd) + ": ", end='')

    try:
        for _ in range(repetitions):
            eprint(".", end='')
            subprocess.run(cmd, stdout=stdout, stderr=stderr, check=True)
    except subprocess.CalledProcessError:
        eprint(f"\b{BOLD}{RED}X{RESET}", end='')

    eprint()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--discard-output", dest="stdout",
                        action="store_const", const=subprocess.DEVNULL,
                        help="discard output",
                        required=False)

    parser.add_argument("-r", "--repetitions",
                        type=int, default=10,
                        help="number of repetitions (default is 10)",
                        required=False)

    parser.add_argument("cmd",
                        nargs="*",
                        help="program to run")

    args = parser.parse_args()

    if args.cmd:
        testrun(args.cmd, args.repetitions, args.stdout)
    else:
        # Read commands from file
        with open("testrun.input") as file:
            for line in file:
                cmd = line.split()
                testrun(cmd, args.repetitions, args.stdout)
