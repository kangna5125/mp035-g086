"""FastAPI service for MP035.

Run locally from the repository root:
    uvicorn app.main:app --host 0.0.0.0 --port 8000
"""
import json
import logging
import sys
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "model.joblib"


class JsonFormatter(logging.Formatter):
    """Write one JSON object per log line."""

    def format(self, record):
        data = {"level": record.levelname, "message": record.getMessage()}
        data.update(getattr(record, "fields", {}))
        return json.dumps(data)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("mp035")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class PredictRequest(BaseModel):
    pm25_today: float
    wind_kmph: float
    humidity_pct: float
    temp_c: float = Field(..., le=70)
    traffic_index: float
    stubble_fires: float = Field(..., ge=0)
    day_type: str
    station_zone: str


app = FastAPI()
model = joblib.load(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(req: PredictRequest):
    row = pd.DataFrame([req.model_dump()])
    prediction = round(float(model.predict(row)[0]), 2)
    logger.info("prediction", extra={"fields": {"station_zone": req.station_zone, "prediction": prediction}})
    return {"prediction": prediction}
