import pandas as pd

from mp035.cleaning import drop_duplicates, drop_leaking_columns, drop_stuck_run


def test_duplicates_are_removed():
    df = pd.DataFrame({"record_id": ["a", "a", "b"], "x": [1, 1, 2]})
    out = drop_duplicates(df)
    assert len(out) == 2


def test_leaking_column_is_dropped():
    df = pd.DataFrame({"x": [1, 2], "pm25_measured_next_day": [5.0, 6.0]})
    out = drop_leaking_columns(df, ["pm25_measured_next_day"])
    assert list(out.columns) == ["x"]


def test_stuck_run_inside_dates_is_removed_only():
    df = pd.DataFrame(
        {
            "date": ["2026-02-17", "2026-02-18", "2026-02-19", "2026-03-10"],
            "pm25_today": [36.8, 36.8, 50.0, 36.8],
        }
    )
    out = drop_stuck_run(df, "pm25_today", 36.8, "2026-02-17", "2026-03-02")
    assert list(out["date"]) == ["2026-02-19", "2026-03-10"]
