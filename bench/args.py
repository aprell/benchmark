import argparse

from bench.metrics import efficiencies, speedups


common = {
    "--all": {
        "action": "store_true",
        "help": "consider all benchmarks in configuration file",
        "required": False,
    },
    "--speedup": {
        "action": "store_const",
        "const": speedups,
        "help": "calculate parallel speedups",
        "required": False,

    },
    "--efficiency": {
        "action": "store_const",
        "const": efficiencies,
        "help": "calculate parallel efficiencies",
        "required": False,
    }
}
