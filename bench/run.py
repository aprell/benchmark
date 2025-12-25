import os

from pathlib import Path

from bench.args import add_argument
from bench.utils import eprint, get_logfile, run as bench_run


def run(cmd, config):
    cmd = cmd.split()

    for n in config.num_threads:
        logfile = get_logfile(cmd, suffix=n, ext="log")
        Path(logfile).parent.mkdir(parents=True, exist_ok=True)

        with open(logfile, "w") as file:
            os.environ.update({
                k: str(n) if v == "$NUM_THREADS" else v
                for k, v in config.environment.items()
            })
            eprint(f"NUM_THREADS={n} ", end='')
            bench_run(cmd, config.repetitions, stdout=file)

    csv_file = get_logfile(cmd, ext="csv")
    if Path(csv_file).exists():
        Path(csv_file).unlink()


def setup(subparsers):
    parser = subparsers.add_parser("run", help="run benchmarks")
    parser.add_argument("cmds", metavar="CMD", nargs="*")
    add_argument(parser, "--all")

    parser.set_defaults(run=main)


def main(args, config):
    for cmd in args.all and config.benchmarks or args.cmds:
        run(cmd, config)
