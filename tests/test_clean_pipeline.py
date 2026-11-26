import pandas as pd

from mp035.cleaning import clean
from mp035.config import load_params


def test_clean_removes_duplicates_stuck_rows_and_leaking_column():
    stuck = load_params()["cleaning"]["stuck_sensor"]
    df = pd.DataFrame(
        {
            "record_id": ["a", "a", "b", "c"],
            "date": ["2026-03-10", "2026-03-10", "2026-02-17", "2026-02-17"],
            "pm25_today": [50.0, 50.0, stuck["value"], 60.0],
            "pm25_measured_next_day": [1.0, 1.0, 2.0, 3.0],
        }
    )
    out = clean(df)
    assert list(out["record_id"]) == ["a", "c"]
    assert "pm25_measured_next_day" not in out.columns
