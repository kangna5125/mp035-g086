"""Train candidate models with MLflow, register the best as v1 and set the champion alias.

Run from the repository root:
    python -m mp035.train
"""
import hashlib

import joblib
import mlflow
import mlflow.sklearn
from mlflow import MlflowClient
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from mp035.cleaning import clean, load_raw, split_xy
from mp035.config import ROOT, load_params


def sha256_file(path):
    """SHA-256 of the original file, read as bytes."""
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def build_estimator(spec, random_state):
    kind = spec["kind"]
    if kind == "ridge":
        return Ridge(alpha=spec["alpha"])
    if kind == "gbr":
        return GradientBoostingRegressor(
            n_estimators=spec["n_estimators"],
            max_depth=spec["max_depth"],
            learning_rate=spec["learning_rate"],
            random_state=random_state,
        )
    if kind == "rf":
        return RandomForestRegressor(
            n_estimators=spec["n_estimators"],
            max_depth=spec["max_depth"],
            random_state=random_state,
        )
    raise ValueError(f"unknown model kind: {kind}")


def build_pipeline(m, estimator):
    """Scale numbers, one-hot encode text, then the model. Same pipeline for train and serve."""
    pre = ColumnTransformer(
        [
            ("num", StandardScaler(), m["features_numeric"]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), m["features_categorical"]),
        ]
    )
    return Pipeline([("pre", pre), ("model", estimator)])


def main():
    params = load_params()
    m = params["model"]
    paths = params["paths"]

    data_sha = sha256_file(ROOT / paths["train_csv"])
    df = clean(load_raw())
    X, y = split_xy(df, params)
    X_tr, X_va, y_tr, y_va = train_test_split(
        X, y, test_size=m["test_size"], random_state=m["random_state"]
    )

    mlflow.set_tracking_uri(paths["mlflow_uri"])
    mlflow.set_experiment(m["experiment"])

    best = None  # (mae, run_id, pipeline, name)
    for spec in m["candidates"]:
        pipe = build_pipeline(m, build_estimator(spec, m["random_state"]))
        with mlflow.start_run(run_name=spec["name"]) as run:
            mlflow.log_param("data_sha256", data_sha)
            mlflow.log_param("candidate", spec["name"])
            mlflow.log_param("n_train_rows", len(X_tr))
            mlflow.log_params({k: v for k, v in spec.items() if k not in ("name", "kind")})

            pipe.fit(X_tr, y_tr)
            mae = mean_absolute_error(y_va, pipe.predict(X_va))
            mlflow.log_metric("mae_val", mae)
            mlflow.sklearn.log_model(pipe, name="model", serialization_format="cloudpickle")

            print(f"{spec['name']}: mae_val={mae:.3f} run_id={run.info.run_id}")
            if best is None or mae < best[0]:
                best = (mae, run.info.run_id, pipe, spec["name"])

    mae, run_id, pipe, name = best
    version = mlflow.register_model(f"runs:/{run_id}/model", m["name"])
    MlflowClient().set_registered_model_alias(m["name"], "champion", version.version)

    model_path = ROOT / paths["model_file"]
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, model_path)

    print(f"\nBest: {name}  mae_val={mae:.3f}")
    print(f"best_run_id: {run_id}")
    print(f"registered: {m['name']} version {version.version} (alias @champion)")
    print(f"data_sha256: {data_sha}")


if __name__ == "__main__":
    main()
