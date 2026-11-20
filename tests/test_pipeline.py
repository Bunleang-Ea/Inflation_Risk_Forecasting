"""
Automated tests. Run from the project root:

    pytest
"""
import pandas as pd
import pytest

from ml import config, service, train
from ml.data.make_dataset import clean, load_raw
from ml.features import add_features


@pytest.fixture(scope="session")
def raw():
    return load_raw()


@pytest.fixture(scope="session")
def cleaned(raw):
    return clean(raw, verbose=False)


@pytest.fixture(scope="session")
def trained_model():
    if not config.MODEL_PATH.exists():
        train.run(verbose=False)
    return config.MODEL_PATH


# --- Data cleaning -----------------------------------------------------------
def test_no_duplicates(cleaned):
    assert cleaned.duplicated().sum() == 0


def test_target_has_valid_values(cleaned):
    assert config.TARGET_COLUMN in cleaned.columns
    assert cleaned[config.TARGET_COLUMN].notna().all()


def test_numbers_are_numeric(cleaned):
    assert pd.api.types.is_numeric_dtype(cleaned["CPI_all_item"])
    assert pd.api.types.is_numeric_dtype(cleaned["YoY_Change_CPI_all_item"])


def test_clean_does_not_change_raw(raw):
    before = raw.copy()
    clean(raw, verbose=False)
    pd.testing.assert_frame_equal(raw, before)


# --- Features ----------------------------------------------------------------
def test_add_features_creates_columns(cleaned):
    out = add_features(cleaned)
    assert {"cpi_momentum_spread", "annualized_mom", "yoy_acceleration_spread"} <= set(out.columns)
    assert len(out) == len(cleaned)


# --- Prediction service ------------------------------------------------------
def _example_input():
    return {f["name"]: f["default"] for f in service.get_schema()["features"]}


def test_prediction_returns_valid_result(trained_model):
    result = service.make_prediction(_example_input())
    assert isinstance(result["prediction"], (int, float))


def test_missing_feature_raises_error(trained_model):
    data = _example_input()
    data.pop(next(iter(data)))
    with pytest.raises(ValueError):
        service.make_prediction(data)


def test_model_beats_minimum_quality(trained_model):
    """Fails if a change makes the model much worse."""
    metrics = service.get_metrics()["test_metrics"]
    if config.TASK_TYPE == "regression":
        assert metrics["r2"] > 0.70
