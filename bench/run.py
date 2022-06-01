import os

from bench.utils import eprint, get_logfile, run as bench_run


def run(cmd, config):
    cmd = cmd.split()

    for n in config.num_threads:
        logfile = get_logfile(cmd, suffix=n, ext="log")
        os.makedirs(os.path.dirname(logfile), exist_ok=True)

        with open(logfile, "w") as file:
            os.environ.update({
                k: str(n) if v == "$NUM_THREADS" else v
                for k, v in config.environment.items()
            })
            eprint(f"NUM_THREADS={n} ", end='')
            bench_run(cmd, config.repetitions, stdout=file)

    csv_file = get_logfile(cmd, ext="csv")
    if os.path.exists(csv_file):
        os.remove(csv_file)


def run_all(config):
    for benchmark in config.benchmarks:
        run(benchmark, config)
