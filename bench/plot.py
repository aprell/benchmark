import matplotlib.pyplot as plt
import numpy as np

from bench.args import add_argument
from bench.stats import get_stats


def plot(cmds, config, outfile, ylabel, xlabel="Number of threads", transform=None):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    for cmd in cmds:
        stats = get_stats(cmd, config)
        if transform:
            stats = transform(stats)
        # Remove column headers
        stats = np.array(stats[1:])

        num_threads = stats[:,0].astype(int)
        median_values = stats[:,4].astype(float)
        lower_errors = median_values - stats[:,2].astype(float)
        upper_errors = stats[:,6].astype(float) - median_values

        plt.errorbar(num_threads,
                     median_values,
                     yerr=[lower_errors, upper_errors],
                     label=cmd.strip("./"))

    plt.legend()
    plt.savefig(outfile)


def setup(subparsers):
    parser = subparsers.add_parser("plot", help="plot benchmark results")
    parser.add_argument("cmds", metavar="CMD", nargs="*")
    parser.add_argument("-o", "--output", metavar="FILE", help="save figure as file", required=False)
    add_argument(parser, "--all")

    metrics = parser.add_mutually_exclusive_group()
    add_argument(metrics, "--speedup")
    add_argument(metrics, "--efficiency")

    parser.set_defaults(run=main)


def main(args, config):
    cmds = args.all and config.benchmarks or args.cmds
    outfile = args.output if args.output else "plot.png"
    metric = args.speedup or args.efficiency
    if args.speedup:
        plot(cmds, config, outfile, ylabel="Speedup", transform=metric)
    elif args.efficiency:
        plot(cmds, config, outfile, ylabel="Efficiency", transform=metric)
    else:
        plot(cmds, config, outfile, ylabel=f"{config.label}")
