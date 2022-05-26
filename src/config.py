import configparser

from .utils import read_list


class Config:
    def __init__(self, configfile):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

        self.benchmarks = read_list(self.config.get("Benchmark", "benchmarks"))
        self.runtimes = read_list(self.config.get("Benchmark", "runtimes"))
        self.num_threads = self.config.get("Benchmark", "num_threads")

        self.environment = {}
        for var, value in self.config["Environment"].items():
            self.environment[var.upper()] = value

        assert(self.num_threads in self.environment)
        self.environment[self.num_threads] = read_list(self.environment[self.num_threads], type=int)

    def print(self):
        print("[Benchmark]")
        print("benchmarks =", self.benchmarks)
        print("runtimes =", self.runtimes)
        print("num_threads =", self.num_threads)
        print("\n[Environment]")
        for k, v in self.environment.items():
            print(k, "=", v)
