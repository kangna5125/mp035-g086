# MP035 - Tomorrow's Air Quality (Indore)

- Group id: G086
- Problem id: MP035
- Course: SCSE3040 MLOps mini project, Batch 7
- Faculty: Dr. Gaurav Tripathi

## Members (enrolment numbers)

| Enrolment | Name |
|---|---|
| S24CSEU0986 | Prathammittal |
| S24CSEU0709 | AVINASHKUMAR |
| S24CSEU0674 | Janwisingh |
| S24CSEU0703 | ARYANTRIPATHI |
| S24CSEU0668 | KANGNABANSAL |

## Setup

```
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src
```

Raw data lives in `data/raw/`. `train.csv` and `later.csv` are tracked with DVC and are not stored in git.

## Pipeline

1. `python -m mp035.data_checks` finds the seven data problems in train.csv.
2. `python -m mp035.train` trains 3 candidate models, logs them to MLflow, registers the best as v1 and sets the `champion` alias.
3. `python -m mp035.monitoring` computes PSI per column and v1 MAE by station zone on later.csv.
4. `python -m mp035.retrain` trains v2 and applies the promotion rule.
5. `python -m mp035.predict_holdout` writes `predictions/holdout_predictions.csv`.

## Tests

```
python -m pytest -q tests
```

## API

Run locally from the repository root:

```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`GET /health` returns `{"status": "ok"}`. `POST /predict` takes the eight fields listed in PROBLEM.md and returns `{"prediction": ...}`.

Docker:

```
docker build -t mp035-api:1.0 .
docker run -p 8000:8000 mp035-api:1.0
```

Kubernetes files are in `k8s/`. Deployment `mp035-api` with 4 replicas, Service `mp035-svc` on port 80.
