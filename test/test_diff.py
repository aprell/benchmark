from bench.config import Config
from bench.diff import actual_diff, relative_diff


def test_actual_diff_a_b(capfd):
    actual_diff(["a/y 30 10", "b/y 30 10"], Config(), color=False)
    assert capfd.readouterr().out == \
"""
 a/y 30 10 vs b/y 30 10
+----------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
| #Threads |     Min     |     P10     |     P25     |   Median    |     P75     |     P90     |     Max     |
+----------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
|    1     |  +8.95 ms   |  +10.99 ms  |  -46.04 ms  |  -69.87 ms  | -116.71 ms  | -160.09 ms  | -159.05 ms  |
|    2     | +1607.34 ms | +1616.25 ms | +1618.98 ms | +1622.80 ms | +1646.79 ms | +1642.68 ms | +1655.53 ms |
|    4     | +1779.59 ms | +1781.14 ms | +2456.98 ms | +3011.18 ms | +3022.45 ms | +3078.80 ms | +3307.06 ms |
|    6     | +1523.77 ms | +1677.13 ms | +1826.51 ms | +1980.84 ms | +2043.90 ms | +2170.31 ms | +2316.84 ms |
|    8     | +1256.21 ms | +1313.89 ms | +1326.25 ms | +1492.19 ms | +1495.66 ms | +1556.87 ms | +1559.21 ms |
+----------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
"""


def test_actual_diff_b_a(capfd):
    actual_diff(["b/y 30 10", "a/y 30 10"], Config(), color=False)
    assert capfd.readouterr().out == \
"""
 b/y 30 10 vs a/y 30 10
+----------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
| #Threads |     Min     |     P10     |     P25     |   Median    |     P75     |     P90     |     Max     |
+----------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
|    1     |  -8.95 ms   |  -10.99 ms  |  +46.04 ms  |  +69.87 ms  | +116.71 ms  | +160.09 ms  | +159.05 ms  |
|    2     | -1607.34 ms | -1616.25 ms | -1618.98 ms | -1622.80 ms | -1646.79 ms | -1642.68 ms | -1655.53 ms |
|    4     | -1779.59 ms | -1781.14 ms | -2456.98 ms | -3011.18 ms | -3022.45 ms | -3078.80 ms | -3307.06 ms |
|    6     | -1523.77 ms | -1677.13 ms | -1826.51 ms | -1980.84 ms | -2043.90 ms | -2170.31 ms | -2316.84 ms |
|    8     | -1256.21 ms | -1313.89 ms | -1326.25 ms | -1492.19 ms | -1495.66 ms | -1556.87 ms | -1559.21 ms |
+----------+-------------+-------------+-------------+-------------+-------------+-------------+-------------+
"""


def test_relative_diff_a_b(capfd):
    relative_diff(["a/y 30 10", "b/y 30 10"], Config(), color=False)
    assert capfd.readouterr().out == \
"""
 a/y 30 10 vs b/y 30 10
+----------+----------+----------+----------+----------+----------+----------+----------+
| #Threads |   Min    |   P10    |   P25    |  Median  |   P75    |   P90    |   Max    |
+----------+----------+----------+----------+----------+----------+----------+----------+
|    1     | +0.07 %  | +0.08 %  | -0.34 %  | -0.51 %  | -0.85 %  | -1.16 %  | -1.15 %  |
|    2     | +23.68 % | +23.80 % | +23.84 % | +23.89 % | +24.23 % | +24.14 % | +24.30 % |
|    4     | +52.08 % | +52.13 % | +71.88 % | +88.08 % | +88.39 % | +90.03 % | +96.70 % |
|    6     | +66.44 % | +73.11 % | +79.62 % | +86.31 % | +88.97 % | +94.35 % | +99.95 % |
|    8     | +72.20 % | +75.47 % | +76.15 % | +85.57 % | +85.64 % | +89.06 % | +89.19 % |
+----------+----------+----------+----------+----------+----------+----------+----------+
"""


def test_relative_diff_b_a(capfd):
    relative_diff(["b/y 30 10", "a/y 30 10"], Config(), color=False)
    assert capfd.readouterr().out == \
"""
 b/y 30 10 vs a/y 30 10
+----------+----------+----------+----------+----------+----------+----------+----------+
| #Threads |   Min    |   P10    |   P25    |  Median  |   P75    |   P90    |   Max    |
+----------+----------+----------+----------+----------+----------+----------+----------+
|    1     | -0.07 %  | -0.08 %  | +0.34 %  | +0.51 %  | +0.85 %  | +1.17 %  | +1.16 %  |
|    2     | -19.14 % | -19.23 % | -19.25 % | -19.28 % | -19.51 % | -19.45 % | -19.55 % |
|    4     | -34.25 % | -34.27 % | -41.82 % | -46.83 % | -46.92 % | -47.38 % | -49.16 % |
|    6     | -39.92 % | -42.23 % | -44.33 % | -46.33 % | -47.08 % | -48.55 % | -49.99 % |
|    8     | -41.93 % | -43.01 % | -43.23 % | -46.11 % | -46.13 % | -47.11 % | -47.14 % |
+----------+----------+----------+----------+----------+----------+----------+----------+
"""
