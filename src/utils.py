import subprocess
import sys


RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, flush=True, **kwargs)


def run(cmd, repetitions=10, stdout=None, stderr=None):
    eprint(" ".join(cmd) + ": ", end='')

    try:
        for _ in range(repetitions):
            eprint(".", end='')
            subprocess.run(cmd, stdout=stdout, stderr=stderr, check=True)
    except subprocess.CalledProcessError:
        eprint(f"\b{BOLD}{RED}X{RESET}", end='')

    eprint()


def read_list(lst, sep=",", elem=str):
    if type(lst) == str:
        return [elem(x.strip()) for x in lst.split(sep)]
    else:
        return lst if type(lst) == list else []
