from bench.metrics import efficiencies, speedups


options = {
    "--all": {
        "action": "store_true",
        "help": "consider all benchmarks in configuration file",
        "required": False,
    },
    "--speedup": {
        "action": "store",
        "const": speedups,
        "nargs": "?",
        "choices": ["invert"],
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


def add_argument(parser, option):
    parser.add_argument(option, **options[option])
