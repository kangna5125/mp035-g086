from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_train_dvc_file_tracks_train_csv_with_md5():
    data = yaml.safe_load((ROOT / "data/raw/train.csv.dvc").read_text())
    out = data["outs"][0]
    assert out["path"] == "train.csv"
    assert out["hash"] == "md5"


def test_raw_csvs_are_ignored_by_git():
    text = (ROOT / "data/raw/.gitignore").read_text()
    assert "/train.csv" in text
    assert "/later.csv" in text
