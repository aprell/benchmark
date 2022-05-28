import os
import subprocess

from bench.utils import run as test_run


def test(cmd, config):
    cmd = cmd.split()
    test_run(cmd, config.repetitions, stdout=subprocess.DEVNULL)


def test_all(config):
    for benchmark in config.benchmarks:
        for runtime in config.runtimes:
            test(os.path.join(runtime, benchmark), config)