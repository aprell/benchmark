import os
import subprocess

from bench.utils import run as test_run


def test(cmd, config):
    cmd = cmd.split()
    test_run(cmd, config.repetitions, stdout=subprocess.DEVNULL)
