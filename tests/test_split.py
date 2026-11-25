import pandas as pd

from mp035.cleaning import split_xy
from mp035.config import load_params


def test_split_xy_separates_target_from_features():
    params = load_params()
    m = params["model"]
    cols = m["features_numeric"] + m["features_categorical"] + [m["target"]]
    df = pd.DataFrame(
        {c: ["weekday", "weekend"] if c in m["features_categorical"] else [1.0, 2.0] for c in cols}
    )
    X, y = split_xy(df, params)
    assert m["target"] not in X.columns
    assert len(y) == 2
