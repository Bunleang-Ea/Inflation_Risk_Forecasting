"""
Project configuration – ONE place to change settings for Inflation Risk Forecasting.
The notebooks, the training script, and both backends read from this file.
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "inflation_data.csv"
PROCESSED_DATA_PATH = ROOT_DIR / "data" / "processed" / "clean.csv"
MODEL_PATH = ROOT_DIR / "models" / "model.joblib"
METRICS_PATH = ROOT_DIR / "models" / "metrics.json"
MODEL_CARD_PATH = ROOT_DIR / "models" / "model_card.md"
FIGURES_DIR = ROOT_DIR / "reports" / "figures"

# ---------------------------------------------------------------------------
# Problem definition
# ---------------------------------------------------------------------------
# "regression"     (forecasting inflation rate YoY %)
# "classification" (forecasting risk regime: High Risk vs Normal)
TASK_TYPE = "regression"

TARGET_COLUMN = "YoY_Change_CPI_all_item"
POSITIVE_CLASS = "High"     # classification fallback
NEGATIVE_CLASS = "Normal"

# Columns that must NOT be used as model inputs (dates, IDs, leakage)
DROP_COLUMNS = ["Date"]

# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
TEST_SIZE = 0.2
CV_FOLDS = 5
RANDOM_STATE = 42

# Metric used to choose the best model
PRIMARY_METRIC = "neg_root_mean_squared_error" if TASK_TYPE == "regression" else "f1"

# Number of random combinations tried when tuning the best model
TUNING_ITERATIONS = 15
