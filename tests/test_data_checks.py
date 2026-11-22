import pandas as pd

from mp035.data_checks import check_duplicates, check_sentinel, check_stuck


def test_duplicates_are_counted():
    df = pd.DataFrame({"record_id": ["a", "a", "b"], "x": [1, 1, 2]})
    assert check_duplicates(df) == {"present": True, "count": 1}


def test_sentinel_is_found():
    df = pd.DataFrame({"temp_c": [20.0] * 5 + [-999.0, -999.0, -999.0, -999.0, -999.0]})
    result = check_sentinel(df)
    assert result["present"] is True
    assert result["value"] == -999


def test_stuck_run_is_found():
    dates = pd.date_range("2026-02-01", periods=8, freq="D").strftime("%Y-%m-%d")
    values = [36.8] * 7 + [50.0]
    df = pd.DataFrame({"date": dates, "pm25_today": values})
    result = check_stuck(df, min_days=7)
    assert result["present"] is True
    assert result["start_date"] == "2026-02-01"
    assert result["end_date"] == "2026-02-07"
