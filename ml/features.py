"""
Step 2 – Feature engineering and preprocessing.

Everything here runs INSIDE the model pipeline, so the API can send the
original (clean) columns and the pipeline creates the new features itself.
"""
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

from ml import config


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create domain-specific macroeconomic momentum features from raw inputs."""
    df = df.copy()

    # 1. Price Momentum Spread: 3-month MA vs 12-month MA
    if {"CPI_3_Month_Moving_Avg", "CPI_12_Month_Moving_Avg"} <= set(df.columns):
        df["cpi_momentum_spread"] = df["CPI_3_Month_Moving_Avg"] - df["CPI_12_Month_Moving_Avg"]

    # 2. Annualized monthly rate: MoM * 12
    if "MoM_Change_CPI_all_item" in df.columns:
        df["annualized_mom"] = df["MoM_Change_CPI_all_item"] * 12.0

    # 3. Short-to-long inflation acceleration: 3M YoY vs 12M YoY
    if {"YoY_3_Month_Avg", "YoY_12_Month_Avg"} <= set(df.columns):
        df["yoy_acceleration_spread"] = df["YoY_3_Month_Avg"] - df["YoY_12_Month_Avg"]

    return df


def get_input_columns(df: pd.DataFrame) -> list[str]:
    """Columns the user/API must provide (before feature engineering)."""
    skip = {config.TARGET_COLUMN, *config.DROP_COLUMNS}
    return [c for c in df.columns if c not in skip]


def split_types(df: pd.DataFrame):
    """Numeric and categorical columns AFTER feature engineering."""
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in df.columns if c not in numeric]
    return numeric, categorical


def build_preprocessor(X_sample: pd.DataFrame) -> Pipeline:
    """add_features ➜ impute ➜ scale / one-hot encode."""
    numeric, categorical = split_types(add_features(X_sample))
    transformers = []
    if numeric:
        transformers.append(
            ("num", Pipeline([
                ("impute", SimpleImputer(strategy="median")),
                ("scale", StandardScaler()),
            ]), numeric)
        )
    if categorical:
        transformers.append(
            ("cat", Pipeline([
                ("impute", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]), categorical)
        )

    columns = ColumnTransformer(transformers)
    return Pipeline([
        ("add_features", FunctionTransformer(add_features)),
        ("columns", columns),
    ])
