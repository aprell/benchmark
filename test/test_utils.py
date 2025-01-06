from pytest import raises

from bench.utils import get_logfile, get_logfiles, get_run_times, read_list


def test_get_logfile():
    assert get_logfile(["x"]) == "benchmark.output/x"
    assert get_logfile(["./x"]) == "benchmark.output/x"
    assert get_logfile(["a/b/c/x"]) == "benchmark.output/a/b/c/x"
    assert get_logfile(["a/b/c/x", "1", "2", "3"]) == "benchmark.output/a/b/c/x_1_2_3"


def test_get_logfile_with_suffix():
    assert get_logfile(["x"], suffix=1) == "benchmark.output/x_001"
    assert get_logfile(["./x"], suffix=2) == "benchmark.output/x_002"
    assert get_logfile(["a/b/c/x"], suffix=3) == "benchmark.output/a/b/c/x_003"
    assert get_logfile(["a/b/c/x", "1", "2", "3"], suffix="4") ==  "benchmark.output/a/b/c/x_1_2_3_4"


def test_get_logfile_with_ext():
    assert get_logfile(["x"], ext="csv") == "benchmark.output/x.csv"
    assert get_logfile(["./x"], ext="log") == "benchmark.output/x.log"
    assert get_logfile(["a/b/c/x"], ext="out") == "benchmark.output/a/b/c/x.out"
    assert get_logfile(["a/b/c/x", "1", "2", "3"], ext="zip") == "benchmark.output/a/b/c/x_1_2_3.zip"


def test_get_logfiles():
    assert get_logfiles(["x"], ext="csv") == []
    assert get_logfiles(["x"], ext="log") == [
        ( 1, "benchmark.output/x_001.log"),
        ( 2, "benchmark.output/x_002.log"),
        ( 4, "benchmark.output/x_004.log"),
        ( 8, "benchmark.output/x_008.log"),
        (16, "benchmark.output/x_016.log")
    ]


def test_get_run_times():
    assert get_run_times("benchmark.output/x_001.log") == [10, 10.1, 9.8]
    assert get_run_times("benchmark.output/x_002.log") == [8, 8.2, 7.9]
    assert get_run_times("benchmark.output/x_004.log") == [6, 5.7, 5.9]
    assert get_run_times("benchmark.output/x_008.log", "=") == [4, 4.3, 4.1]
    assert get_run_times("benchmark.output/x_016.log", ">") == [3.2]

    with raises(FileNotFoundError):
        get_run_times("benchmark.output/x_032.log")


def test_read_list():
    assert read_list([]) == []
    assert read_list("") == [""]
    assert read_list("1") == ["1"]
    assert read_list("1 , 2 , 3") == ["1", "2", "3"]
    assert read_list("1 | 2 | 3", sep="|", elem=int) == [1, 2, 3]
