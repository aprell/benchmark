from bench.config import Config


def test_config_01():
    config = Config("config.input/01.ini")
    assert config.benchmarks == []
    assert config.num_threads == [1]
    assert config.repetitions == 10
    assert config.environment == {}


def test_config_02():
    config = Config("config.input/02.ini")
    assert config.benchmarks == []
    assert config.num_threads == [1, 2, 4, 8, 16]
    assert config.repetitions == 10
    assert config.environment == {
        "OMP_NUM_THREADS": "$NUM_THREADS"
    }


def test_config_03():
    config = Config("config.input/03.ini")
    assert config.benchmarks == ["x", "y", "z"]
    assert config.num_threads == [1, 2, 4, 8, 16]
    assert config.repetitions == 5
    assert config.match == '"Elapsed time"'
    assert config.unit == "us"
    assert config.environment == {
        "OMP_PLACES": "cores",
        "OMP_PROC_BIND": "close",
        "OMP_NUM_THREADS": "$NUM_THREADS"
    }
