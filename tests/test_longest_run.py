import pandas as pd

from mp035.data_checks import longest_run


def test_longest_run_finds_the_consecutive_block():
    days = list(pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-10", "2026-01-11"]))
    start, end, length = longest_run(days)
    assert str(start.date()) == "2026-01-01"
    assert str(end.date()) == "2026-01-03"
    assert length == 3


def test_a_gap_breaks_the_run():
    days = list(pd.to_datetime(["2026-01-01", "2026-01-03"]))
    assert longest_run(days)[2] == 1
