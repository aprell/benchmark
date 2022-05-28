import configparser

from bench.utils import read_list


class Config:
    def __init__(self, configfile):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

        self.benchmarks = read_list(self.config.get("Benchmark", "benchmarks", fallback=[]))
        self.runtimes = read_list(self.config.get("Benchmark", "runtimes", fallback=[]))
        self.num_threads = read_list(self.config.get("Benchmark", "num_threads", fallback=[1]), elem=int)
        self.repetitions = self.config.getint("Benchmark", "repetitions", fallback=10)

        self.environment = {}
        if "Environment" in self.config:
            for var, value in self.config["Environment"].items():
                self.environment[var.upper()] = value

    def print(self):
        print("[Benchmark]")
        print("benchmarks =", self.benchmarks)
        print("runtimes =", self.runtimes)
        print("num_threads =", self.num_threads)
        print("repetitions =", self.repetitions)
        print("\n[Environment]")
        for k, v in self.environment.items():
            print(k, "=", v)
