"""Find the seven kinds of data problem in train.csv.

Run from the repository root:
    python -m mp035.data_checks

Every answer printed here is computed from your own files.
"""
import re

import pandas as pd
import yaml

from mp035.config import ROOT, load_params

NUMERIC = [
    "pm25_today",
    "wind_kmph",
    "humidity_pct",
    "temp_c",
    "traffic_index",
    "stubble_fires",
    "pm25_measured_next_day",
    "pm25_next_day",
]
NUMERIC_FEATURES = [c for c in NUMERIC if c not in ("pm25_measured_next_day", "pm25_next_day")]
TEXT = ["day_type", "station_zone"]
GROUP = "station_zone"
TARGET = "pm25_next_day"
SENTINELS = [-1, -999, 999, 9999]


def longest_run(days):
    """Longest run of consecutive calendar days in a sorted list of Timestamps."""
    best_start = start = prev = days[0]
    best_end = prev
    best_len = run = 1
    for d in days[1:]:
        if (d - prev).days == 1:
            run += 1
        else:
            start, run = d, 1
        prev = d
        if run > best_len:
            best_start, best_end, best_len = start, d, run
    return best_start, best_end, best_len


def check_leaking(df, holdout_cols):
    """A column missing from holdout that almost copies the target."""
    for col in df.columns:
        if col in ("record_id", "date", TARGET) or col in holdout_cols:
            continue
        if pd.api.types.is_numeric_dtype(df[col]):
            corr = df[col].corr(df[TARGET])
            if abs(corr) > 0.95:
                return {"present": True, "column": col, "correlation": round(float(corr), 4)}
    return {"present": False}


def check_unit_mixup(df, tolerance=0.1):
    """One station_zone recorded a feature at a very different scale from the others."""
    for col in NUMERIC_FEATURES:
        if col not in df.columns:
            continue
        for zone, sub in df.groupby(GROUP):
            others = df.loc[df[GROUP] != zone, col].median()
            if others == 0:
                continue
            ratio = sub[col].median() / others
            if ratio >= 5 or ratio <= 0.2:
                factor = round(ratio if ratio >= 5 else 1 / ratio)
                return {"present": True, "column": col, "group_value": zone, "factor": factor}
    return {"present": False}


def check_sentinel(df):
    """A special number typed instead of a real reading."""
    for col in NUMERIC:
        if col not in df.columns:
            continue
        for s in SENTINELS:
            n = int((df[col] == s).sum())
            if n >= 5:
                return {"present": True, "column": col, "value": s, "count": n}
    return {"present": False}


def check_duplicates(df):
    """Extra copies of the same row (rows you would delete)."""
    n = int(df.duplicated().sum())
    return {"present": n > 0, "count": n}


def check_stuck(df, min_days=7):
    """One value repeated on a long run of consecutive days."""
    dates = pd.to_datetime(df["date"])
    best = None
    for col in NUMERIC:
        if col not in df.columns:
            continue
        for value, idx in df.groupby(col).groups.items():
            days = sorted(set(dates.loc[idx].dt.normalize()))
            start, end, length = longest_run(days)
            if length >= min_days and (best is None or length > best["days"]):
                best = {
                    "present": True,
                    "column": col,
                    "value": float(value),
                    "start_date": start.date().isoformat(),
                    "end_date": end.date().isoformat(),
                    "days": length,
                }
    return best or {"present": False}


def check_target_typos(df, factor=5):
    """Targets typed about 10 times too big sit far above the rest."""
    median = df[TARGET].median()
    count = int((df[TARGET] > factor * median).sum())
    return {"present": count > 0, "count": count, "max_target": float(df[TARGET].max())}


def _normalise(value):
    return re.sub(r"[^a-z]", "", str(value).lower())


def check_spelling(df):
    """The same category written in different ways."""
    for col in TEXT:
        if col not in df.columns:
            continue
        raw = df[col].dropna().unique()
        groups = {}
        for v in raw:
            groups.setdefault(_normalise(v), set()).add(v)
        if len(raw) > len(groups):
            return {"present": True, "column": col, "true_levels": len(groups)}
    return {"present": False}


def run_all():
    params = load_params()
    train = pd.read_csv(ROOT / params["paths"]["train_csv"])
    holdout_cols = list(pd.read_csv(ROOT / params["paths"]["holdout_csv"], nrows=1).columns)
    return {
        "leaking_column": check_leaking(train, holdout_cols),
        "unit_mixup": check_unit_mixup(train),
        "sentinel_value": check_sentinel(train),
        "duplicate_rows": check_duplicates(train),
        "stuck_sensor": check_stuck(train),
        "target_typos": check_target_typos(train),
        "spelling_variants": check_spelling(train),
    }


def main():
    print(yaml.safe_dump(run_all(), sort_keys=False))


if __name__ == "__main__":
    main()
