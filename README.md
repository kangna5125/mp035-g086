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
```

Raw data lives in `data/raw/` (train.csv and later.csv are tracked with DVC and
are not in git; run `dvc pull` after cloning if you have a remote).

## Pipeline

1. `python -m mp035.data_checks` - finds the seven data problems in train.csv
2. `python -m mp035.train` - trains 3 candidate models, logs them to MLflow,
   registers the best as v1 and sets the `champion` alias
