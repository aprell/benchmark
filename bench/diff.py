import numpy as np

from bench.stats import get_stats, print_table
from bench.utils import GREEN as GOOD, RED as BAD, RESET


def format_number(n, suffix="", color=True):
    if color:
        return f"{BAD}+{n:.2f}{suffix}{RESET}" if n > 0 else f"{GOOD}{n:.2f}{suffix}{RESET}"
    else:
        return f"+{n:.2f}{suffix}" if n > 0 else f"{n:.2f}{suffix}"


def __actual_diff(a, b):
    return a - b


def __relative_diff(a, b):
    return (a - b) / b * 100


def actual_diff(cmds, config, color=True):
    def format(n):
        return format_number(n, suffix=f" {config.unit}", color=color)
    diff(cmds, config, func=__actual_diff, format=format)


def relative_diff(cmds, config, color=True):
    def format(n):
        return format_number(n, suffix=" %", color=color)
    diff(cmds, config, func=__relative_diff, format=format)


def diff(cmds, config, func, format):
    a = np.array(get_stats(cmds[0], config))
    b = np.array(get_stats(cmds[1], config))
    d = np.vectorize(format)(func(a[1:,1:-4].astype(float), b[1:,1:-4].astype(float)))
    print("\n", cmds[0], "vs", cmds[1])
    print_table(np.r_[[a[0,:-4]], np.c_[a[1:,0], d]].tolist())
