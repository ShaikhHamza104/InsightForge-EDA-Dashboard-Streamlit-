from __future__ import annotations

import numpy as np
import pandas as pd

import streamlit as st

# Optional fancyimpute support
try:
    from fancyimpute import KNN as FancyKNN  # type: ignore
    FANCYIMPUTE_AVAILABLE = True
except Exception:
    FancyKNN = None
    FANCYIMPUTE_AVAILABLE = False


def fancyimpute_available() -> bool:
    return FANCYIMPUTE_AVAILABLE


def safe_knn_neighbors(n_rows: int, default: int = 5) -> int:
    # KNN requires at least 2 rows (n_neighbors <= n_rows-1)
    if n_rows <= 1:
        return 0
    return min(default, max(1, n_rows - 1))


@st.cache_data(show_spinner=False)
def numeric_describe(numeric_df: pd.DataFrame) -> pd.DataFrame:
    return numeric_df.describe()


def numeric_knn_impute(df_numeric: pd.DataFrame, n_neighbors: int = 5) -> pd.DataFrame:
    # Use sklearn KNNImputer (imported lazily to keep helpers light)
    from sklearn.impute import KNNImputer  # local import to avoid global dependency during import time

    rows = df_numeric.shape[0]
    k = safe_knn_neighbors(rows, default=n_neighbors)
    if k <= 0:
        raise ValueError("Not enough rows to perform KNN imputation.")
    imputer = KNNImputer(n_neighbors=k)
    imputed = imputer.fit_transform(df_numeric)
    return pd.DataFrame(imputed, columns=df_numeric.columns, index=df_numeric.index)


def encode_categoricals_label(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, "LabelEncoder"]]:
    # Label encode each categorical col but keep NaNs as NaN (floats)
    from sklearn.preprocessing import LabelEncoder  # local import

    encoders: dict[str, LabelEncoder] = {}
    encoded = pd.DataFrame(index=df.index)

    for col in df.columns:
        series = df[col]
        non_null = series.dropna()
        if non_null.empty:
            # Keep the column as all-NaN float
            encoded[col] = pd.Series(np.nan, index=df.index, dtype=float)
            continue

        le = LabelEncoder()
        le.fit(non_null.astype(str))
        encoders[col] = le

        out = pd.Series(np.nan, index=df.index, dtype=float)
        mask = series.notna()
        if mask.any():
            out.loc[mask] = le.transform(series.loc[mask].astype(str))
        encoded[col] = out

    return encoded, encoders


def fancy_knn_impute_categoricals(encoded_df: pd.DataFrame, k: int = 3) -> pd.DataFrame:
    if not FANCYIMPUTE_AVAILABLE or FancyKNN is None:
        raise ImportError("fancyimpute is not available.")

    rows = encoded_df.shape[0]
    k_eff = safe_knn_neighbors(rows, default=k)
    if k_eff <= 0:
        raise ValueError("Not enough rows to perform fancyimpute KNN imputation.")

    imputer = FancyKNN(k=k_eff)
    imputed = imputer.fit_transform(encoded_df.values)
    return pd.DataFrame(imputed, columns=encoded_df.columns, index=encoded_df.index)


def decode_labels_to_strings(imputed_encoded_df: pd.DataFrame, encoders: dict[str, "LabelEncoder"]) -> pd.DataFrame:
    decoded = pd.DataFrame(index=imputed_encoded_df.index)
    for col in imputed_encoded_df.columns:
        if col not in encoders:
            decoded[col] = imputed_encoded_df[col]
            continue
        le = encoders[col]
        vals = np.round(imputed_encoded_df[col]).astype(int)
        vals = np.clip(vals, 0, len(le.classes_) - 1)
        decoded[col] = le.inverse_transform(vals)
    return decoded


def missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    counts = df.isnull().sum()
    total = len(df) if len(df) else 1
    perc = (counts / total * 100).round(2)
    out = pd.DataFrame({"Column": counts.index.astype(str), "Missing Count": counts.values, "Missing Percentage": perc.values})
    return out


def high_missing_columns(df: pd.DataFrame, threshold: float = 0.5) -> list[str]:
    # threshold is fraction (e.g., 0.5 for 50%)
    if df.shape[0] == 0:
        return []
    perc = df.isnull().sum() / df.shape[0]
    return perc[perc > threshold].index.astype(str).tolist()