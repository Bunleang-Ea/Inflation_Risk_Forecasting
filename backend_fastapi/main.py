"""
FastAPI backend.  Run from the PROJECT ROOT folder:

    uvicorn backend_fastapi.main:app --reload --port 8000

Interactive API docs: http://localhost:8000/docs
"""
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml import service

app = FastAPI(title="Project API", version="1.0")

# Simple in-memory prediction history (resets when the server restarts).
# TODO: save to a real database (SQLite + SQLAlchemy/SQLModel) if your scope needs it.
PREDICTION_LOG: list[dict] = []

# Allow the Streamlit frontend (and others) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictRequest(BaseModel):
    features: dict[str, Any]

    model_config = {
        "json_schema_extra": {
            "example": {"features": {
                "CPI_all_item": 211.53, "MoM_Change_CPI_all_item": 0.58,
                "CPI_3_Month_Moving_Avg": 211.05, "CPI_12_Month_Moving_Avg": 208.99,
                "YoY_3_Month_Avg": 1.39, "YoY_12_Month_Avg": 2.52}}
        }
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "backend": "fastapi"}


@app.get("/api/schema")
def schema():
    return service.get_schema()


@app.get("/api/data")
def data(limit: int = 100):
    return service.get_data(limit)


@app.get("/api/metrics")
def metrics():
    report = service.get_metrics()
    if report is None:
        raise HTTPException(404, "Model is not trained yet.")
    return report


@app.post("/api/train")
def train():
    return service.train_model()


@app.post("/api/predict")
def predict(req: PredictRequest):
    try:
        result = service.make_prediction(req.features)
    except RuntimeError as e:
        raise HTTPException(409, str(e))
    except ValueError as e:
        raise HTTPException(422, str(e))
    PREDICTION_LOG.insert(0, {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "input": req.features,
        "prediction": str(result["prediction"]),
        "probabilities": result.get("probabilities"),
    })
    return result


@app.get("/api/predictions")
def prediction_history():
    return {"items": PREDICTION_LOG[:50]}


# TODO: add endpoints for the other features in your scope sheet,
# e.g. user login, saving prediction history, CRUD for your own data.
