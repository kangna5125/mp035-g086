"""Cleaning rules for train.csv. Each rule comes from a finding in data_checks.py."""
import pandas as pd

from mp035.config import ROOT, load_params


def load_raw(path=None):
    """Read the original train.csv exactly as given (never edit it in Excel)."""
    params = load_params()
    path = ROOT / (path or params["paths"]["train_csv"])
    return pd.read_csv(path)


def drop_duplicates(df):
    """Remove extra copies of the same row."""
    return df.drop_duplicates().reset_index(drop=True)


def drop_stuck_run(df, column, value, start, end):
    """Remove rows where a stuck sensor repeated `value` between start and end (inclusive)."""
    dates = pd.to_datetime(df["date"])
    stuck = (df[column] == value) & (dates >= pd.Timestamp(start)) & (dates <= pd.Timestamp(end))
    return df.loc[~stuck].reset_index(drop=True)


def drop_leaking_columns(df, columns):
    """Remove columns that are only known after the event (they would leak the answer)."""
    return df.drop(columns=[c for c in columns if c in df.columns])


def clean(df, params=None):
    """Apply all cleaning rules in order and return a new DataFrame."""
    params = params or load_params()
    c = params["cleaning"]
    df = drop_duplicates(df)
    s = c["stuck_sensor"]
    df = drop_stuck_run(df, s["column"], s["value"], s["start_date"], s["end_date"])
    df = drop_leaking_columns(df, c["leaking_columns"])
    return df.reset_index(drop=True)


def split_xy(df, params=None):
    """Return (features, target) using the column lists in params.yaml."""
    params = params or load_params()
    m = params["model"]
    X = df[m["features_numeric"] + m["features_categorical"]]
    y = df[m["target"]]
    return X, y
