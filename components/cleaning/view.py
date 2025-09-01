from __future__ import annotations

import pandas as pd
import streamlit as st

from .sections import (
    ui_categorical_imputation,
    ui_dataset_overview,
    ui_drop_columns,
    ui_drop_high_missing_columns,
    ui_missing_overview,
    ui_numeric_imputation,
)


class BasicDataClean:
    """Interactive data cleaning component. Works on a copy of the provided DataFrame."""

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy() if df is not None else df

    # Backward-compatible method names used in main.py
    def drop_high_missing_columns(self):
        ui_drop_high_missing_columns(self)

    def drop_columns(self):
        ui_drop_columns(self)

    def display_cleaning_interface(self):
        st.title("🧹 Basic Data Cleaning")

        if self.df is None or self.df.empty:
            st.warning("⚠️ No data available for cleaning. Please upload a dataset first.")
            return None

        ui_dataset_overview(self.df)

        missing_cols_df = ui_missing_overview(self.df)
        if missing_cols_df.empty:
            # Still show a small preview and return
            st.subheader("🔍 Data Preview")
            st.write(f"Shape: {self.df.shape}")
            st.dataframe(self.df.head(), use_container_width=True)
            st.success("✅ Nothing to clean. Dataset has no missing values.")
            return self.df

        # Tabs for separate strategies
        tab1, tab2 = st.tabs(["🔢 Numeric Columns", "📝 Categorical Columns"])
        with tab1:
            ui_numeric_imputation(self)
        with tab2:
            ui_categorical_imputation(self)

        # Results
        st.header("📋 Cleaning Results")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Before Cleaning")
            before_missing = int(missing_cols_df["Missing Count"].sum())
            st.write(f"Missing values: {before_missing:,}")
        with col2:
            st.subheader("After Cleaning")
            after_missing = int(self.df.isnull().sum().sum())
            st.write(f"Missing values: {after_missing:,}")

        st.subheader("🔍 Data Preview After Cleaning")
        st.write(f"Shape: {self.df.shape}")
        st.dataframe(self.df.head(), use_container_width=True)

        if after_missing == 0:
            st.success("✅ All missing values have been handled!")
        else:
            st.warning(f"⚠️ {after_missing:,} missing values remain.")

        return self.df