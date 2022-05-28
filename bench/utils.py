import glob
import os
import re
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


def get_num_threads(env):
    """
    Get the value of environment variable `env` if defined, else get the number of CPUs from `lscpu`
    """
    num_threads = os.environ.get(env)
    if not num_threads:
        num_threads = subprocess.check_output("lscpu | grep ^CPU\(s\)", shell=True).split()[1]
    return int(num_threads)


def get_logfile(cmd, suffix=None, ext=None):
    logdir = os.path.join("benchmark.output", os.path.dirname(cmd[0]))
    logfile = os.path.join(logdir, os.path.basename(cmd[0]))
    if len(cmd) > 1:
        logfile += "_" + "_".join(cmd[1:])
    if suffix:
        if type(suffix) == int:
            logfile += f"_{suffix:03}"
        else:
            logfile += f"_{suffix}"
    if ext:
        logfile += f".{ext}"
    return logfile


def get_logfiles(cmd, ext=None):
    def get_num_threads(logfile):
        return int(os.path.splitext(logfile)[0][-3:])
    pattern = get_logfile(cmd) + "*"
    if ext:
        pattern += f".{ext}"
    logfiles = glob.glob(pattern)
    return [(get_num_threads(logfile), logfile) for logfile in sorted(logfiles)]


def get_run_times(logfile):
    run_times = []
    with open(logfile) as file:
        elapsed = re.compile(r"[^:]*: *(\d+(?:\.\d*)?)")
        for line in file:
            match = re.search(elapsed, line)
            if match:
                run_times.append(float(match.group(1)))
    return run_times


def read_list(lst, sep=",", elem=str):
    if type(lst) == str:
        return [elem(x.strip()) for x in lst.split(sep)]
    else:
        return lst if type(lst) == list else []