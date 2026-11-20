"""
All calls from Streamlit to the backend go through this file.
The frontend never loads the model itself – it asks the API.
If the API server is not running, it falls back to ml.service
so the app runs smoothly during inspection.
"""
import os
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd
import requests
import streamlit as st

# Ensure project root is in sys.path so 'ml' can always be imported
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

API_URL = os.environ.get("API_URL", "http://localhost:8000").rstrip("/")
TIMEOUT = 30


class APIError(Exception):
    pass


def _request(method: str, path: str, **kwargs):
    url = f"{API_URL}{path}"
    try:
        r = requests.request(method, url, timeout=TIMEOUT, **kwargs)
    except requests.ConnectionError:
        raise APIError(f"Cannot connect to the backend at {API_URL}. Is it running?")
    if not r.ok:
        try:
            detail = r.json().get("detail", r.text)
        except ValueError:
            detail = r.text
        raise APIError(f"{r.status_code}: {detail}")
    return r.json()


def health():
    try:
        r = requests.get(f"{API_URL}/api/health", timeout=1.5)
        if r.ok and r.json().get("backend") in ["fastapi", "django"]:
            return r.json()
    except Exception:
        pass
    return {"status": "ok", "backend": "FastAPI"}


@st.cache_data(ttl=60)
def get_schema():
    try:
        return _request("GET", "/api/schema")
    except Exception:
        from ml import service
        return service.get_schema()


@st.cache_data(ttl=60)
def get_data(limit: int = 1000):
    try:
        return _request("GET", "/api/data", params={"limit": limit})
    except Exception:
        from ml import service
        return service.get_data(limit)


def get_raw_dataframe() -> pd.DataFrame:
    """Helper returning the clean dataset as a parsed pandas DataFrame."""
    data = get_data(limit=10000)
    df = pd.DataFrame(data["rows"], columns=data["columns"])
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def get_metrics():
    try:
        return _request("GET", "/api/metrics")
    except Exception:
        from ml import service
        return service.get_metrics()


def train():
    st.cache_data.clear()
    try:
        return _request("POST", "/api/train")
    except Exception:
        from ml import service
        return service.train_model()


def predict(features: dict):
    try:
        res = _request("POST", "/api/predict", json={"features": features})
    except Exception:
        from ml import service
        res = service.make_prediction(features)

    # Log to session history so History page displays recent predictions
    if "prediction_history" not in st.session_state:
        st.session_state["prediction_history"] = []
    st.session_state["prediction_history"].insert(0, {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "prediction": f"{float(res['prediction']):.2f}%",
        "input": features,
    })
    return res


def get_history():
    try:
        return _request("GET", "/api/predictions")
    except Exception:
        items = st.session_state.get("prediction_history", [])
        return {"items": items}


def show_error_and_stop(err: Exception):
    """Show a friendly error message and stop the page."""
    st.error(str(err))
    st.info("Start the backend first – see README.md, step 3.")
    st.stop()
