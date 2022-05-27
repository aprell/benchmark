import sys


RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, flush=True, **kwargs)


def read_list(lst, sep=",", elem=str):
    if type(lst) == str:
        return [elem(x.strip()) for x in lst.split(sep)]
    else:
        return lst if type(lst) == list else []
