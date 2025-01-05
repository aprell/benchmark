from bench.args import add_argument
from bench.stats import get_stats, print_csv, print_table


def report(cmd, config, transform=None, tabulate=True):
    print("\n", cmd, f"({config.label})")
    stats = get_stats(cmd, config)
    if transform:
        stats = transform(stats)
    print_table(stats) if tabulate else print_csv(stats)


def setup(subparsers):
    parser = subparsers.add_parser("report", help="report benchmark results")
    parser.add_argument("cmds", metavar="CMD", nargs="*")
    add_argument(parser, "--all")

    metrics = parser.add_mutually_exclusive_group()
    add_argument(metrics, "--speedup")
    add_argument(metrics, "--efficiency")

    parser.set_defaults(run=main)


def main(args, config):
    metric = args.speedup or args.efficiency
    for cmd in args.all and config.benchmarks or args.cmds:
        report(cmd, config, transform=metric)
