from importlib.metadata import entry_points
from setuptools import find_packages, setup


setup(
    name = "benchmark",
    version = "0.0.1",
    author = "Andreas Prell",
    author_email = "andreas.h.prell@gmail.com",
    description = "Benchmark Utilities",
    packages = find_packages(),
    entry_points = {
        "console_scripts": ["bench=bench.main:main"]
    },
)
