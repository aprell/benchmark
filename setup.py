from importlib.metadata import entry_points
import setuptools


setuptools.setup(
    name="benchmark",
    version="0.0.1",
    author="Andreas Prell",
    author_email="andreas.h.prell@gmail.com",
    description="Benchmarking Utilities",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": ["bench=bench:main"]
    },
)
