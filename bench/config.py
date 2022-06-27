import configparser

from bench.utils import read_list


class Config:
    def __init__(self, configfile="bench.ini"):
        self.config = configparser.ConfigParser()
        self.config.read(configfile)

        # [Benchmark]
        self.benchmarks = read_list(self.config.get("Benchmark", "benchmarks", fallback=[]))
        self.num_threads = read_list(self.config.get("Benchmark", "num_threads", fallback=[1]), elem=int)
        self.repetitions = self.config.getint("Benchmark", "repetitions", fallback=10)

        # [Time]
        self.match = self.config.get("Time", "match", fallback=r"[^:]*")
        self.unit = self.config.get("Time", "unit", fallback="ms")

        # [Environment]
        self.environment = {}
        if "Environment" in self.config:
            for var, value in self.config["Environment"].items():
                self.environment[var.upper()] = value

    def print(self):
        print("[Benchmark]")
        print("benchmarks =", self.benchmarks)
        print("num_threads =", self.num_threads)
        print("repetitions =", self.repetitions)
        print("\n[Time]")
        print("match =", self.match)
        print("unit =", self.unit)
        print("\n[Environment]")
        for k, v in self.environment.items():
            print(k, "=", v)
