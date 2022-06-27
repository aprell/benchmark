from bench.config import Config
from bench.metrics import efficiencies, speedups
from bench.report import report


def test_report_run_time_a(capfd):
    report("a/y 30 10", Config())
    assert capfd.readouterr().out == \
"""
 a/y 30 10 (ms)
+----------+----------+---------+---------+----------+----------+---------+---------+---------+---------+---------+-------------------+
| #Threads |   Min    |   P10   |   P25   |  Median  |   P75    |   P90   |   Max   | P75-P25 | P90-P10 | Max-Min |    Mean ± RSD     |
+----------+----------+---------+---------+----------+----------+---------+---------+---------+---------+---------+-------------------+
|    1     | 13628.25 | 13634.6 | 13641.3 | 13645.23 | 13650.66 | 13665.8 | 13667.8 |  9.36   |  31.21  |  39.55  | 13647.01 ± 0.09 % |
|    2     | 8395.69  | 8406.89 | 8410.54 | 8416.69  | 8442.22  | 8447.28 | 8467.77 |  31.67  |  40.39  |  72.08  | 8425.41 ± 0.26 %  |
|    4     | 5196.35  | 5198.05 | 5874.95 | 6429.76  | 6441.97  | 6498.46 | 6727.14 | 567.02  | 1300.41 | 1530.79 |  6145.2 ± 9.18 %  |
|    6     | 3817.35  | 3971.11 | 4120.66 | 4275.85  | 4341.31  | 4470.64 | 4634.94 | 220.65  | 499.52  | 817.59  | 4242.31 ± 5.49 %  |
|    8     | 2996.08  | 3054.93 | 3067.9  | 3236.05  |  3242.1  | 3305.04 | 3307.43 |  174.2  | 250.11  | 311.35  |  3176.42 ± 3.6 %  |
+----------+----------+---------+---------+----------+----------+---------+---------+---------+---------+---------+-------------------+
"""


def test_report_speedup_a(capfd):
    report("a/y 30 10", Config(), speedups)
    assert capfd.readouterr().out == \
"""
 a/y 30 10 (ms)
+----------+------+------+------+--------+------+------+------+
| #Threads | Min  | P10  | P25  | Median | P75  | P90  | Max  |
+----------+------+------+------+--------+------+------+------+
|    1     | 1.0  | 1.0  | 1.0  |  1.0   | 1.0  | 1.0  | 1.0  |
|    2     | 1.61 | 1.62 | 1.62 |  1.62  | 1.62 | 1.62 | 1.63 |
|    4     | 2.03 | 2.1  | 2.12 |  2.12  | 2.32 | 2.63 | 2.63 |
|    6     | 2.94 | 3.05 | 3.14 |  3.19  | 3.31 | 3.44 | 3.57 |
|    8     | 4.13 | 4.13 | 4.21 |  4.22  | 4.45 | 4.47 | 4.55 |
+----------+------+------+------+--------+------+------+------+
"""


def test_report_efficiency_a(capfd):
    report("a/y 30 10", Config(), efficiencies)
    assert capfd.readouterr().out == \
"""
 a/y 30 10 (ms)
+----------+------+------+------+--------+------+------+------+
| #Threads | Min  | P10  | P25  | Median | P75  | P90  | Max  |
+----------+------+------+------+--------+------+------+------+
|    1     | 1.0  | 1.0  | 1.0  |  1.0   | 1.0  | 1.0  | 1.0  |
|    2     | 0.81 | 0.81 | 0.81 |  0.81  | 0.81 | 0.81 | 0.81 |
|    4     | 0.51 | 0.52 | 0.53 |  0.53  | 0.58 | 0.66 | 0.66 |
|    6     | 0.49 | 0.51 | 0.52 |  0.53  | 0.55 | 0.57 | 0.6  |
|    8     | 0.52 | 0.52 | 0.53 |  0.53  | 0.56 | 0.56 | 0.57 |
+----------+------+------+------+--------+------+------+------+
"""


def test_report_run_time_b(capfd):
    report("b/y 30 10", Config())
    assert capfd.readouterr().out == \
"""
 b/y 30 10 (ms)
+----------+---------+----------+----------+---------+----------+----------+----------+---------+---------+---------+-------------------+
| #Threads |   Min   |   P10    |   P25    | Median  |   P75    |   P90    |   Max    | P75-P25 | P90-P10 | Max-Min |    Mean ± RSD     |
+----------+---------+----------+----------+---------+----------+----------+----------+---------+---------+---------+-------------------+
|    1     | 13619.3 | 13623.61 | 13687.34 | 13715.1 | 13767.37 | 13825.89 | 13826.85 |  80.02  | 202.28  | 207.55  | 13722.81 ± 0.53 % |
|    2     | 6788.35 | 6790.64  | 6791.56  | 6793.89 | 6795.43  |  6804.6  | 6812.24  |  3.87   |  13.96  |  23.89  |  6795.7 ± 0.1 %   |
|    4     | 3416.76 | 3416.91  | 3417.97  | 3418.58 | 3419.52  | 3419.66  | 3420.08  |  1.55   |  2.74   |  3.32   | 3418.56 ± 0.03 %  |
|    6     | 2293.58 | 2293.98  | 2294.15  | 2295.01 | 2297.41  | 2300.33  |  2318.1  |  3.26   |  6.35   |  24.52  | 2297.71 ± 0.32 %  |
|    8     | 1739.87 | 1741.04  | 1741.65  | 1743.86 | 1746.44  | 1748.17  | 1748.22  |  4.79   |  7.13   |  8.35   | 1744.16 ± 0.17 %  |
+----------+---------+----------+----------+---------+----------+----------+----------+---------+---------+---------+-------------------+
"""


def test_report_speedup_b(capfd):
    report("b/y 30 10", Config(), speedups)
    assert capfd.readouterr().out == \
"""
 b/y 30 10 (ms)
+----------+------+------+------+--------+------+------+------+
| #Threads | Min  | P10  | P25  | Median | P75  | P90  | Max  |
+----------+------+------+------+--------+------+------+------+
|    1     | 0.99 | 0.99 | 1.0  |  1.0   | 1.0  | 1.01 | 1.01 |
|    2     | 2.01 | 2.02 | 2.02 |  2.02  | 2.02 | 2.02 | 2.02 |
|    4     | 4.01 | 4.01 | 4.01 |  4.01  | 4.01 | 4.01 | 4.01 |
|    6     | 5.92 | 5.96 | 5.97 |  5.98  | 5.98 | 5.98 | 5.98 |
|    8     | 7.85 | 7.85 | 7.85 |  7.86  | 7.87 | 7.88 | 7.88 |
+----------+------+------+------+--------+------+------+------+
"""


def test_report_efficiency_b(capfd):
    report("b/y 30 10", Config(), efficiencies)
    assert capfd.readouterr().out == \
"""
 b/y 30 10 (ms)
+----------+------+------+------+--------+------+------+------+
| #Threads | Min  | P10  | P25  | Median | P75  | P90  | Max  |
+----------+------+------+------+--------+------+------+------+
|    1     | 0.99 | 0.99 | 1.0  |  1.0   | 1.0  | 1.01 | 1.01 |
|    2     | 1.01 | 1.01 | 1.01 |  1.01  | 1.01 | 1.01 | 1.01 |
|    4     | 1.0  | 1.0  | 1.0  |  1.0   | 1.0  | 1.0  | 1.0  |
|    6     | 0.99 | 0.99 | 0.99 |  1.0   | 1.0  | 1.0  | 1.0  |
|    8     | 0.98 | 0.98 | 0.98 |  0.98  | 0.98 | 0.98 | 0.99 |
+----------+------+------+------+--------+------+------+------+
"""
