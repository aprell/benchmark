from src.config import Config


def test_config_01():
    config = Config("config.input/01.cfg")
    assert not config.benchmarks
    assert not config.runtimes
    assert not config.num_threads
    assert not config.environment
    assert config.repetitions == 10


def test_config_02():
    config = Config("config.input/02.cfg")
    assert not config.benchmarks
    assert not config.runtimes
    assert config.num_threads == "OMP_NUM_THREADS"
    assert config.environment["OMP_NUM_THREADS"] == [1, 2, 4, 8, 16]
    assert config.repetitions == 10


def test_config_03():
    config = Config("config.input/03.cfg")
    assert config.benchmarks == ["x", "y", "z"]
    assert config.runtimes == ["a", "b", "c"]
    assert config.num_threads == "OMP_NUM_THREADS"
    assert config.environment["OMP_NUM_THREADS"] == [1, 2, 4, 8, 16]
    assert config.repetitions == 5
