"""
Step 1 – Data cleaning:  data/raw/  ➜  data/processed/clean.csv

Run from the project root:

    python -m ml.data.make_dataset
"""
import numpy as np
import pandas as pd

from ml import config


def load_raw(path=config.RAW_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def clean(df: pd.DataFrame, verbose: bool = True) -> pd.DataFrame:
    """Return a cleaned copy of the raw inflation data."""
    log = []
    df = df.copy()

    # 1. Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    log.append(f"Removed {before - len(df)} duplicate rows")

    # 2. Strip column whitespace
    df.columns = [c.strip() for c in df.columns]

    # 3. Format Date
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.sort_values("Date").reset_index(drop=True)
        log.append("Sorted records chronologically by Date")

    # 4. Ensure numeric columns are properly formatted numbers
    numeric_cols = [
        "CPI_all_item",
        "MoM_Change_CPI_all_item",
        "YoY_Change_CPI_all_item",
        "CPI_3_Month_Moving_Avg",
        "CPI_12_Month_Moving_Avg",
        "YoY_3_Month_Avg",
        "YoY_12_Month_Avg",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 5. Drop rows missing the target
    before = len(df)
    df = df.dropna(subset=[config.TARGET_COLUMN])
    log.append(f"Dropped {before - len(df)} rows with missing target")

    if verbose:
        print("\n".join("  - " + line for line in log))
        print(f"  Clean shape: {df.shape}")
    return df.reset_index(drop=True)


def main():
    raw = load_raw()
    print(f"Raw shape: {raw.shape}")
    df = clean(raw)
    config.PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.PROCESSED_DATA_PATH, index=False)
    print(f"Saved ➜ {config.PROCESSED_DATA_PATH.relative_to(config.ROOT_DIR)}")


if __name__ == "__main__":
    main()
