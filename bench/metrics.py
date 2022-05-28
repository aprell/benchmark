import numpy as np


def transform(func):
    def apply(stats, base=None):
        # Remove column headers and last four columns
        headers = stats[0][:-4]
        numbers = np.array(stats)[1:,:-4].astype(float)
        # Add back column headers
        return [headers] + func(numbers)
    return apply


@transform
def speedups(numbers, base=None):
    base = base if base else numbers[0][4]
    return [[int(n), *reversed([base/x for x in xs])] for n, *xs in numbers]


@transform
def efficiencies(numbers, base=None):
    base = base if base else numbers[0][4]
    return [[int(n), *reversed([base/x/n for x in xs])] for n, *xs in numbers]
