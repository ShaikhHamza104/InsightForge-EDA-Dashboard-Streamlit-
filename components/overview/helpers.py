import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def cached_describe(numeric_df: pd.DataFrame) -> pd.DataFrame:
    """Cached describe (non-transposed)."""
    return numeric_df.describe()


@st.cache_data(ttl=180, show_spinner=False)
def cached_corr(numeric_df: pd.DataFrame, method: str) -> pd.DataFrame:
    """Cached correlation matrix with selected method."""
    return numeric_df.corr(method=method, numeric_only=True)


@st.cache_data(ttl=180, show_spinner=False)
def cached_value_counts(series: pd.Series, dropna: bool) -> pd.Series:
    """Cached value counts for a Series."""
    return series.value_counts(dropna=dropna)