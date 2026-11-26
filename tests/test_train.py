import pandas as pd

from mp035.config import load_params
from mp035.train import build_estimator, build_pipeline, sha256_file


def test_build_estimator_ridge_uses_alpha():
    est = build_estimator({"kind": "ridge", "alpha": 2.5}, 42)
    assert est.alpha == 2.5


def test_pipeline_fits_and_predicts_one_value_per_row():
    m = load_params()["model"]
    pipe = build_pipeline(m, build_estimator({"kind": "ridge", "alpha": 1.0}, 42))
    rows = 6
    df = pd.DataFrame({c: list(range(rows)) for c in m["features_numeric"]})
    df["day_type"] = ["weekday", "weekend"] * 3
    df["station_zone"] = ["Central", "Industrial", "Residential"] * 2
    y = [float(i) for i in range(rows)]
    pipe.fit(df[m["features_numeric"] + m["features_categorical"]], y)
    preds = pipe.predict(df[m["features_numeric"] + m["features_categorical"]])
    assert len(preds) == rows


def test_sha256_is_64_hex_characters(tmp_path):
    f = tmp_path / "x.txt"
    f.write_text("abc")
    digest = sha256_file(f)
    assert len(digest) == 64
    assert all(c in "0123456789abcdef" for c in digest)
