import os

import matplotlib.pyplot as plt
import numpy as np

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
                     label=os.path.dirname(cmd).upper())

    plt.legend()
    plt.savefig(outfile)
